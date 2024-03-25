import re

from pyspark.errors import PySparkException
from pyspark.sql import DataFrame

from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
from databricks.labs.remorph.reconcile.constants import SourceDriver
from databricks.labs.remorph.reconcile.recon_config import JdbcReaderOptions, Schema


class SnowflakeDataSource(DataSource):

    @property
    def get_jdbc_url(self) -> str:
        return (
            f"jdbc:{self.source}://{self._get_secrets('account')}.snowflakecomputing.com"
            f"/?user={self._get_secrets('sfUser')}&password={self._get_secrets('sfPassword')}"
            f"&db={self._get_secrets('sfDatabase')}&schema={self._get_secrets('sfSchema')}"
            f"&warehouse={self._get_secrets('sfWarehouse')}&role={self._get_secrets('sfRole')}"
        )

    def read_data(self, catalog: str, schema: str, query: str, options: JdbcReaderOptions) -> DataFrame:
        try:

            table_query = self._get_table_or_query(catalog, schema, query)

            if options is None:
                return self.reader(table_query)

            options = self._get_jdbc_reader_options(options)
            return (
                self._get_jdbc_reader(table_query, self.get_jdbc_url, SourceDriver.SNOWFLAKE.value)
                .options(**options)
                .load()
            )
        except PySparkException as e:
            error_msg = (
                f"An error occurred while fetching Snowflake Data using the following {query} in "
                f"SnowflakeDataSource : {e!s}"
            )
            raise PySparkException(error_msg) from e

    def get_schema(self, catalog: str, schema: str, table: str) -> list[Schema]:
        try:
            schema_query = self.get_schema_query(catalog, schema, table)
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
    def get_schema_query(catalog_name: str, schema_name: str, table_name: str):
        query = f"""select column_name, case when numeric_precision is not null and numeric_scale is not null then 
        concat(data_type, '(', numeric_precision, ',' , numeric_scale, ')') when lower(data_type) = 'text' then 
        concat('varchar', '(', CHARACTER_MAXIMUM_LENGTH, ')')  else data_type end as data_type from 
        {catalog_name}.INFORMATION_SCHEMA.COLUMNS where lower(table_name)='{table_name}' 
        and lower(table_schema) = '{schema_name}' order by ordinal_position"""
        return re.sub(r'\s+', ' ', query)

    snowflake_datatype_mapper = {}
