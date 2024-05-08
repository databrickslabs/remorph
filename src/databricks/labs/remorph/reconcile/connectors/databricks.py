import re

from pyspark.errors import PySparkException
from pyspark.sql import DataFrame
from pyspark.sql.functions import col

from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
from databricks.labs.remorph.reconcile.recon_config import JdbcReaderOptions, Schema


class DatabricksDataSource(DataSource):
    def read_data(self, catalog: str, schema: str, query: str, options: JdbcReaderOptions) -> DataFrame:
        try:
            table_query = self._get_table_or_query(catalog, schema, query)
            df = self.spark.sql(table_query)
            return df.select([col(column).alias(column.lower()) for column in df.columns])
        except PySparkException as e:
            error_msg = (
                f"An error occurred while fetching Databricks Data using the following {table_query} in "
                f"DatabricksDataSource : {e!s}"
            )
            raise PySparkException(error_msg) from e

    def get_schema(self, catalog: str, schema: str, table: str) -> list[Schema]:
        try:
            schema_query = self.get_schema_query(catalog, schema, table)
            schema_df = self.spark.sql(schema_query).where("col_name not like '#%'").distinct()
            return [Schema(field.col_name.lower(), field.data_type.lower()) for field in schema_df.collect()]
        except PySparkException as e:
            error_msg = (
                f"An error occurred while fetching Databricks Schema using the following "
                f"{schema_query} query in DatabricksDataSource: {e!s}"
            )
            raise PySparkException(error_msg) from e

    @staticmethod
    def get_schema_query(catalog: str, schema: str, table: str):
        # TODO: Ensure that the target_catalog in the configuration is not set to "hive_metastore". The source_catalog
        #  can only be set to "hive_metastore" if the source type is "databricks".
        if catalog == "hive_metastore":
            return f"describe table {schema}.{table}"

        query = f"""select lower(column_name) as col_name, full_data_type as data_type from 
                    {catalog}.information_schema.columns where lower(table_catalog)='{catalog}' 
                    and lower(table_schema)='{schema}' and lower(table_name) ='{table}' order by 
                    col_name"""
        return re.sub(r'\s+', ' ', query)

    databricks_datatype_mapper = {}
