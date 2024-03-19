from pyspark.sql import DataFrame

from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
from databricks.labs.remorph.reconcile.constants import SourceDriver
from databricks.labs.remorph.reconcile.recon_config import Schema, Tables


class SnowflakeDataSource(DataSource):

    @property
    def get_jdbc_url(self) -> str:
        url = f"jdbc:{self.source}://{self.connection_params['account']}.snowflakecomputing.com/?user={self.connection_params['sfUser']}&password={self.connection_params['sfPassword']}&db={self.connection_params['sfDatabase']}&schema={self.connection_params['sfSchema']}&warehouse={self.connection_params['sfWarehouse']}"
        if 'sfRole' in self.connection_params:
            url = url + f"&role={self.connection_params['sfRole']}"
        return url

    def read_data(self, schema_name: str, catalog_name: str, table_or_query: str, table_conf: Tables) -> DataFrame:
        try:
            if table_conf.jdbc_reader_options is None:
                return self.reader(table_or_query)

            return (
                self._get_jdbc_reader(table_or_query, self.get_jdbc_url, SourceDriver.SNOWFLAKE.value)
                .options(**self._get_jdbc_reader_options(table_conf.jdbc_reader_options))
                .load()
            )
        except PySparkException as e:
            error_msg = f"An error occurred while fetching Snowflake Data using the following {table_or_query} in SnowflakeDataSource : {e!s}"
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
            .options(**self.connection_params)
            .load()
        )

    @staticmethod
    def _get_schema_query(table_name: str, schema_name: str, catalog_name: str):
        return f""" select column_name, case when numeric_precision is not null and numeric_scale is not null then concat(data_type, '(', numeric_precision, ',' , numeric_scale, ')') 
        when lower(data_type) = 'text' then concat('varchar', '(', CHARACTER_MAXIMUM_LENGTH, ')')  else data_type end as data_type from 
        {catalog_name}.INFORMATION_SCHEMA.COLUMNS where lower(table_name)='{table_name}' and lower(table_schema) = '{schema_name}' order by ordinal_position
        """
