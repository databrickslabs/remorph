import logging
from dataclasses import asdict

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StructType
from sqlglot import parse_one

from databricks.labs.remorph.config import MorphConfig
from databricks.labs.remorph.reconcile.constants import Constants, SourceType
from databricks.labs.remorph.reconcile.recon_config import (
    Schema,
    SchemaMatchResult,
    SchemCompareOutput,
    Table,
)

logger = logging.getLogger(__name__)


class SchemaCompare:
    def __init__(
        self,
        source_schema: list[Schema],
        databricks_schema: list[Schema],
        source: str,
        table_conf: Table,
        spark: SparkSession,
    ):
        self.source_schema = source_schema
        self.databricks_schema = databricks_schema
        self.source = source
        self.table_conf = table_conf
        self.spark = spark

    def _build_master_schema(self) -> list[SchemaMatchResult]:
        master_schema = self.source_schema
        if self.table_conf.select_columns:
            master_schema = [s for s in master_schema if s.column_name in self.table_conf.select_columns]
        if self.table_conf.drop_columns:
            master_schema = [s for s in master_schema if s.column_name not in self.table_conf.drop_columns]

        target_column_map = self.table_conf.to_src_col_map or {}
        master_schema = [
            SchemaMatchResult(
                source_column=s.column_name,
                databricks_column=target_column_map.get(s.column_name, s.column_name),
                source_datatype=s.data_type,
                databricks_datatype=next(
                    (
                        tgt.data_type
                        for tgt in self.databricks_schema
                        if tgt.column_name == target_column_map.get(s.column_name, s.column_name)
                    ),
                    "",
                ),
            )
            for s in master_schema
        ]
        return master_schema

    def _create_dataframe(self, data: list, schema: StructType) -> DataFrame:
        """
        :param data: Expectation is list of dataclass
        :param schema: Target schema
        :return: DataFrame
        """
        data = [tuple(asdict(item).values()) for item in data]
        df = self.spark.createDataFrame(data, schema)

        return df

    def _parse(self, column: str, data_type: str) -> str:
        config = MorphConfig(source=self.source)
        return (
            parse_one(f"create table dummy ({column} {data_type})", read=config.get_read_dialect())
            .sql(dialect=config.get_write_dialect())
            .replace(", ", ",")
        )

    @classmethod
    def _all_valid(cls, schema_compare_maps: list[SchemaMatchResult]) -> bool:
        return bool(all(x.is_valid for x in schema_compare_maps))

    @classmethod
    def _validate_parsed_query(cls, master: SchemaMatchResult, parsed_query) -> None:
        databricks_query = f"create table dummy ({master.source_column} {master.databricks_datatype})"
        logger.info(
            f"""
        Snowflake datatype: create table dummy ({master.source_column} {master.source_datatype})
        Parse datatype: {parsed_query}
        Databricks datatype: {databricks_query}
        """
        )
        if parsed_query.lower() != databricks_query.lower():
            master.is_valid = False

    def compare(self) -> SchemCompareOutput:
        """
        This method compares the source schema and the Databricks schema. It checks if the data types of the columns in the source schema
        match with the corresponding columns in the Databricks schema by parsing using remorph transpile.

        Returns:
            SchemCompareOutput: A dataclass object containing a boolean indicating the overall result of the comparison and a DataFrame with the comparison details.
        """
        master_schema = self._build_master_schema()
        for master in master_schema:
            if self.source.upper() != SourceType.DATABRICKS.value:
                parsed_query = self._parse(master.source_column, master.source_datatype)
                self._validate_parsed_query(master, parsed_query)
            elif master.source_datatype.lower() != master.databricks_datatype.lower():
                master.is_valid = False

        df = self._create_dataframe(master_schema, Constants.schema_compare)
        final_result = self._all_valid(master_schema)
        return SchemCompareOutput(final_result, df)
