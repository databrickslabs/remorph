from pyspark.sql import DataFrame

from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
from databricks.labs.remorph.reconcile.recon_config import JdbcReaderOptions, Schema


class SnowflakeDataSource(DataSource):
    def read_data(self, catalog: str, schema: str, query: str, options: JdbcReaderOptions) -> DataFrame:
        # Implement Snowflake-specific logic here
        return NotImplemented

    def get_schema(self, catalog: str, schema: str, table: str) -> list[Schema]:
        # Implement Snowflake-specific logic here
        return NotImplemented

    snowflake_datatype_mapper = {}
