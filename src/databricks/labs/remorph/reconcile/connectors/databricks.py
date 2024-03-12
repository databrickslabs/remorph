from pyspark.sql import DataFrame

from databricks.labs.remorph.reconcile.connectors.data_source import DataSource


class DatabricksDataSource(DataSource):
    def read_data(self, table_name: str, schema_name: str, catalog_name: str, query: str) -> DataFrame:
        # Implement Databricks-specific logic here
        return NotImplemented

    def get_schema(self, table_name: str, schema_name: str, catalog_name: str) -> dict[str, str]:
        # Implement Databricks-specific logic here
        return NotImplemented

    databricks_datatype_mapper = {}
