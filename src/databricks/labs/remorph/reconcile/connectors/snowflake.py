from pyspark.sql import DataFrame

from databricks.labs.remorph.reconcile.connectors.data_source import DataSource


class SnowflakeDataSource(DataSource):
    def read_data(self, table_name: str, schema_name: str, catalog_name: str, query: str) -> DataFrame:
        # Implement Snowflake-specific logic here
        return NotImplemented

    def get_schema(self, table_name: str, schema_name: str, catalog_name: str) -> dict[str, str]:
        # Implement Snowflake-specific logic here
        return NotImplemented

    snowflake_datatype_mapper = {}
