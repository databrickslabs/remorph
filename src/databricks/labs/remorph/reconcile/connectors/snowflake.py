from pyspark.errors import PySparkException
from pyspark.sql import DataFrame

from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
from databricks.labs.remorph.reconcile.constants import SourceDriver
from databricks.labs.remorph.reconcile.recon_config import Schema, Tables


class SnowflakeDataSource(DataSource):

    @property
    def get_jdbc_url(self) -> str:
        return (
            f"jdbc:{self.source}://{self._get_secrets('account')}.snowflakecomputing.com"
            f"/?user={self._get_secrets('sfUser')}&password={self._get_secrets('sfPassword')}"
            f"&db={self._get_secrets('sfDatabase')}&schema={self._get_secrets('sfSchema')}"
            f"&warehouse={self._get_secrets('sfWarehouse')}&role={self._get_secrets('sfRole')}"
        )

    def read_data(self, schema_name: str, catalog_name: str, query: str, table_conf: Tables) -> DataFrame:
        try:
            if table_conf.jdbc_reader_options is None:
                return self.reader(query)

            return (
                self._get_jdbc_reader(query, self.get_jdbc_url, SourceDriver.SNOWFLAKE.value)
                .options(**self._get_jdbc_reader_options(table_conf.jdbc_reader_options))
                .load()
            )
        except PySparkException as e:
            error_msg = f"An error occurred while fetching Snowflake Data using the following {query} in SnowflakeDataSource : {e!s}"
            raise PySparkException(error_msg) from e

    def get_schema(self, table_name: str, schema_name: str, catalog_name: str) -> list[Schema]:
        try:
            schema_query = self._get_schema_query(table_name, schema_name, catalog_name)
            schema_df = self.reader(schema_query).load()
            return [Schema(field.column_name.lower(), field.data_type.lower()) for field in schema_df.collect()]
        except PySparkException as e:
            error_msg = (
                f"An error occurred while fetching Snowflake Schema using the following {table_name} in "
                f"SnowflakeDataSource: {e!s}"
            )
            raise PySparkException(error_msg) from e

    def reader(self, query: str) -> DataFrame:
        return (
            self.spark.read.format("snowflake")
            .option("dbtable", f"({query}) as tmp")
            .option("sfUrl", self._get_secrets('sfUrl'))
            .option("sfUser", self._get_secrets('sfUser'))
            .option("sfPassword", self._get_secrets('sfPassword'))
            .option("sfDatabase", self._get_secrets('sfDatabase'))
            .option("sfSchema", self._get_secrets('sfSchema'))
            .option("sfWarehouse", self._get_secrets('sfWarehouse'))
            .option("sfRole", self._get_secrets('sfRole'))
            .load()
        )

    @staticmethod
    def _get_schema_query(table_name: str, schema_name: str, catalog_name: str):
        return f""" select column_name, case when numeric_precision is not null and numeric_scale is not null then concat(data_type, '(', numeric_precision, ',' , numeric_scale, ')') 
        when lower(data_type) = 'text' then concat('varchar', '(', CHARACTER_MAXIMUM_LENGTH, ')')  else data_type end as data_type from 
        {catalog_name}.INFORMATION_SCHEMA.COLUMNS where lower(table_name)='{table_name}' and lower(table_schema) = '{schema_name}' order by ordinal_position
        """

    snowflake_datatype_mapper = {}
