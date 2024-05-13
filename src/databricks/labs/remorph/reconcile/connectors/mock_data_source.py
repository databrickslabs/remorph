from pyspark.sql import DataFrame

from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
from databricks.labs.remorph.reconcile.recon_config import JdbcReaderOptions, Schema


class MockDataSource(DataSource):

    def __init__(
        self,
        dataframe_repository: dict[(str, str, str), DataFrame],
        schema_repository: dict[(str, str, str), list[Schema]],
    ):
        self._dataframe_repository: dict[(str, str, str), DataFrame] = dataframe_repository
        self._schema_repository: dict[(str, str, str), list[Schema]] = schema_repository

    def read_query_data(
        self, catalog: str, schema: str, table: str, query: str, options: JdbcReaderOptions | None
    ) -> DataFrame:
        mock_df = self._dataframe_repository.get((catalog, schema, query))
        if not mock_df:
            raise ValueError(f"data is not mocked for the combination : {(catalog, schema, query)}")
        return mock_df

    def get_schema(self, catalog: str, schema: str, table: str) -> list[Schema]:
        mock_schema = self._schema_repository.get((catalog, schema, table))
        if not mock_schema:
            raise ValueError(f"schema is not mocked for the combination : {(catalog, schema, table)}")
        return mock_schema
