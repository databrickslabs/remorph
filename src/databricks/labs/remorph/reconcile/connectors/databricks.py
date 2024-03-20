from pyspark.errors import PySparkException
from pyspark.sql import DataFrame
from pyspark.sql.functions import col

from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
from databricks.labs.remorph.reconcile.recon_config import Schema, Tables


class DatabricksDataSource(DataSource):
    def read_data(self, schema_name: str, catalog_name: str, query: str, table_conf: Tables) -> DataFrame:
        try:
            df = self.spark.sql(query)
            df = df.select([col(column).alias(column.lower()) for column in df.columns])
            return df
        except PySparkException as e:
            error_msg = f"An error occurred while fetching Databricks Data using the following {query} in DatabricksDataSource : {e!s}"
            raise PySparkException(error_msg) from e

    def get_schema(self, table_name: str, schema_name: str, catalog_name: str) -> list[Schema]:
        try:
            full_table_name = (
                f"{catalog_name}.{schema_name}.{table_name}" if catalog_name else f"{schema_name}.{table_name}"
            )
            schema_df = self.spark.sql(f"describe table {full_table_name}").where("col_name not like '#%'").distinct()
            return [Schema(field.col_name.lower(), field.data_type.lower()) for field in schema_df.collect()]
        except PySparkException as e:
            error_msg = (
                f"An error occurred while fetching Databricks Schema using the following {catalog_name}.{schema_name}.{table_name} in "
                f"DatabricksDataSource: {e!s}"
            )
            raise PySparkException(error_msg) from e

    databricks_datatype_mapper = {}
