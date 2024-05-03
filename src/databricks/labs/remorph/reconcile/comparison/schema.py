import logging
from dataclasses import dataclass

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import BooleanType, StringType, StructField, StructType
from sqlglot import parse_one

from databricks.labs.remorph.config import MorphConfig
from databricks.labs.remorph.reconcile.constants import SourceType
from databricks.labs.remorph.reconcile.recon_config import Schema, Table


@dataclass
class SchemaCompareMap:
    source_column: str
    source_data_type: str
    databricks_column: str
    databricks_data_type: str
    is_valid: bool = True


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

    def _build_master(self) -> list[SchemaCompareMap]:
        master_schema = self.source_schema
        if self.table_conf.select_columns:
            master_schema = [s for s in master_schema if s.column_name in self.table_conf.select_columns]
        if self.table_conf.drop_columns:
            master_schema = [s for s in master_schema if s.column_name not in self.table_conf.drop_columns]

        target_column_map = self.table_conf.to_src_col_map or {}
        master_schema = [
            SchemaCompareMap(
                source_column=s.column_name,
                databricks_column=target_column_map.get(s.column_name, ''),
                source_data_type=s.data_type,
                databricks_data_type=next(
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

    def _create_dataframe(self, schema_compare_maps: list[SchemaCompareMap]) -> DataFrame:
        # Define the schema for the DataFrame
        schema = StructType(
            [
                StructField("source_column", StringType(), True),
                StructField("source_data_type", StringType(), True),
                StructField("databricks_column", StringType(), True),
                StructField("databricks_data_type", StringType(), True),
                StructField("is_valid", BooleanType(), True),
            ]
        )
        # Convert list of dataclass objects to list of tuples
        data = [
            (
                item.source_column,
                item.source_data_type,
                item.databricks_column,
                item.databricks_data_type,
                item.is_valid,
            )
            for item in schema_compare_maps
        ]
        # Create DataFrame
        df = self.spark.createDataFrame(data, schema)
        return df

    # TODO : Once we have inline sql parse functions in transpiler we have to replace this
    def _parse(self, column: str, data_type: str) -> str:
        config = MorphConfig(source=self.source)
        return (
            parse_one(f"create table dummy ({column} {data_type})", read=config.get_read_dialect())
            .sql(dialect=config.get_write_dialect())
            .replace(", ", ",")
        )

    @classmethod
    def _all_valid(cls, schema_compare_maps: list[SchemaCompareMap]) -> str:
        return "Success" if all(x.is_valid for x in schema_compare_maps) else "Failed"

    @classmethod
    def _validate_parsed_query(cls, master, parsed_query):
        databricks_query = f"create table dummy ({master.source_column} {master.databricks_data_type})"
        logger.info(
            f"""
        Snowflake datatype: create table dummy ({master.source_column} {master.source_data_type})
        Parse datatype: {parsed_query}
        Databricks datatype: {databricks_query}
        """
        )
        if parsed_query.lower() != databricks_query.lower():
            master.is_valid = False

    def compare(self) -> tuple[str, DataFrame]:
        master_schema = self._build_master()
        for master in master_schema:
            if self.source.upper() != SourceType.DATABRICKS.value:
                parsed_query = self._parse(master.source_column, master.source_data_type)
                self._validate_parsed_query(master, parsed_query)
            elif master.source_data_type.lower() != master.databricks_data_type.lower():
                master.is_valid = False

        df = self._create_dataframe(master_schema)
        final_result = self._all_valid(master_schema)
        return final_result, df
