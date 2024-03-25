from pyspark.sql import DataFrame

from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
from databricks.labs.remorph.reconcile.recon_config import JdbcReaderOptions, Schema


class DatabricksDataSource(DataSource):
    def read_data(self, catalog: str, schema: str, query: str, options: JdbcReaderOptions) -> DataFrame:
        # Implement Databricks-specific logic here
        return NotImplemented

    def get_schema(self, catalog: str, schema: str, table: str) -> list[Schema]:
        # Implement Databricks-specific logic here
        return NotImplemented

    databricks_datatype_mapper = {}
