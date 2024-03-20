from pyspark.sql import DataFrame

from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
from databricks.labs.remorph.reconcile.recon_config import Schema, Tables


class DatabricksDataSource(DataSource):
    def read_data(self, schema_name: str, catalog_name: str, query: str, table_conf: Tables) -> DataFrame:
        # Implement Databricks-specific logic here
        return NotImplemented

    def get_schema(self, table_name: str, schema_name: str, catalog_name: str) -> list[Schema]:
        # Implement Databricks-specific logic here
        return NotImplemented

    databricks_datatype_mapper = {}
