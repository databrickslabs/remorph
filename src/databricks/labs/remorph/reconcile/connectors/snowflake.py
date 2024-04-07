import re

from pyspark.errors import PySparkException
from pyspark.sql import DataFrame
from pyspark.sql.functions import col

from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
from databricks.labs.remorph.reconcile.constants import SourceDriver, SourceType
from databricks.labs.remorph.reconcile.recon_config import (
    JdbcReaderOptions,
    Schema,
    Table,
    TableRecon,
)
from databricks.labs.blueprint.entrypoint import get_logger

logger = get_logger(__file__)


class SnowflakeDataSource(DataSource):
    @property
    def get_jdbc_url(self) -> str:
        jdbc_url = (
            f"jdbc:{SourceType.SNOWFLAKE.value}://{self._get_secrets('account')}.snowflakecomputing.com"
            f"/?user={self._get_secrets('sfUser')}&password={self._get_secrets('sfPassword')}"
            f"&db={self._get_secrets('sfDatabase')}&schema={self._get_secrets('sfSchema')}"
            f"&warehouse={self._get_secrets('sfWarehouse')}&role={self._get_secrets('sfRole')}"
        )
        logger.debug(f"JDBC URL: {jdbc_url}")
        return jdbc_url

    def read_data(self, catalog: str, schema: str, query: str, options: JdbcReaderOptions) -> DataFrame:
        try:
            table_query = self._get_table_or_query(catalog, schema, query)

            logger.debug(f"Fetching Snowflake Data using the following {query} in SnowflakeDataSource")
            if options is None:
                df = self.reader(table_query)
            else:
                options = self._get_jdbc_reader_options(options)
                df = (
                    self._get_jdbc_reader(table_query, self.get_jdbc_url, SourceDriver.SNOWFLAKE.value)
                    .options(**options)
                    .load()
                )
            return df.select([col(column).alias(column.lower()) for column in df.columns])
        except PySparkException as e:
            error_msg = (
                f"An error occurred while fetching Snowflake Data using the following {query} in "
                f"SnowflakeDataSource : {e!s}"
            )
            raise PySparkException(error_msg) from e

    def get_schema(self, catalog: str, schema: str, table: str) -> list[Schema]:
        try:
            schema_query = self.get_schema_query(catalog, schema, table)
            logger.info(f"Fetching Snowflake Schema using the following {table} in SnowflakeDataSource")
            schema_df = self.reader(schema_query).load()
            return [Schema(field.column_name.lower(), field.data_type.lower()) for field in schema_df.collect()]
        except PySparkException as e:
            error_msg = (
                f"An error occurred while fetching Snowflake Schema using the following {table} in "
                f"SnowflakeDataSource: {e!s}"
            )
            raise PySparkException(error_msg) from e

    def reader(self, query: str) -> DataFrame:
        options = {
            "sfUrl": self._get_secrets('sfUrl'),
            "sfUser": self._get_secrets('sfUser'),
            "sfPassword": self._get_secrets('sfPassword'),
            "sfDatabase": self._get_secrets('sfDatabase'),
            "sfSchema": self._get_secrets('sfSchema'),
            "sfWarehouse": self._get_secrets('sfWarehouse'),
            "sfRole": self._get_secrets('sfRole'),
        }
        return self.spark.read.format("snowflake").option("dbtable", f"({query}) as tmp").options(**options).load()

    @staticmethod
    def get_schema_query(catalog: str, schema: str, table: str):
        query = f"""select column_name, case when numeric_precision is not null and numeric_scale is not null then 
        concat(data_type, '(', numeric_precision, ',' , numeric_scale, ')') when lower(data_type) = 'text' then 
        concat('varchar', '(', CHARACTER_MAXIMUM_LENGTH, ')')  else data_type end as data_type from 
        {catalog}.INFORMATION_SCHEMA.COLUMNS where lower(table_name)='{table}' 
        and lower(table_schema) = '{schema}' order by ordinal_position"""
        return re.sub(r'\s+', ' ', query)

    def list_tables(
            self,
            catalog: str,
            schema: str,
            include_list: list[str] | None,
            exclude_list: list[str] | None,
    ) -> TableRecon:

        filter_list = include_list
        in_clause = "IN"
        if exclude_list:
            filter_list = exclude_list
            in_clause = "NOT IN"

        subset_tables = ", ".join(filter_list)

        where_cond = f"AND TABLE_NAME {in_clause} ({subset_tables})" if filter_list else ""

        try:
            logger.info(f"Fetching Snowflake Table list for `{catalog}.{schema}`")
            tables_query = f"""SELECT TABLE_NAME, CLUSTERING_KEY, ROW_COUNT\n 
                               FROM {catalog.upper()}.INFORMATION_SCHEMA.TABLES\n 
                               WHERE TABLE_SCHEMA = '{schema.upper()}' {where_cond}"""

            logger.info(f" Executing query: {tables_query}")
            tables_df = self.reader(tables_query).load()

            tables_list = [
                Table(source_name=field.TABLE_NAME.lower(), target_name=field.TABLE_NAME.lower())
                for field in tables_df.collect()
            ]
            table_recon = TableRecon(
                source_catalog=catalog, source_schema=schema, target_catalog="", target_schema="", tables=tables_list
            )

            return table_recon
        except PySparkException as e:
            error_msg = (
                f"An error occurred while fetching Snowflake Table list for `{catalog}.{schema}`  in "
                f"SnowflakeDataSource: {e!s}"
            )
            raise PySparkException(error_msg) from e

    snowflake_datatype_mapper = {}
