import logging
from abc import ABC, abstractmethod

from pyspark.sql import DataFrame

from databricks.labs.remorph.reconcile.exception import DataSourceRuntimeException
from databricks.labs.remorph.reconcile.recon_config import JdbcReaderOptions, Schema

logger = logging.getLogger(__name__)


def _raise_runtime_exception(exception: Exception, fetch_type: str, query: str) -> DataSourceRuntimeException:
    error_msg = f"Runtime exception occurred while fetching {fetch_type} using {query} : {exception}"
    return DataSourceRuntimeException(error_msg)


def log_and_throw_exception(exception: Exception, fetch_type: str, query: str):
    logger.warning(str(_raise_runtime_exception(exception, fetch_type, query)))
    print(str(_raise_runtime_exception(exception, fetch_type, query)))


class DataSource(ABC):

    @abstractmethod
    def read_data(
        self, catalog: str, schema: str, table: str, query: str, options: JdbcReaderOptions | None
    ) -> DataFrame:
        return NotImplemented

    @abstractmethod
    def get_schema(self, catalog: str, schema: str, table: str) -> list[Schema]:
        return NotImplemented


class MockDataSource(DataSource):

    def __init__(
        self,
        dataframe_repository: dict[(str, str, str), DataFrame],
        schema_repository: dict[(str, str, str), list[Schema]],
        exception: Exception = RuntimeError("Mock Exception"),
    ):
        self._dataframe_repository: dict[(str, str, str), DataFrame] = dataframe_repository
        self._schema_repository: dict[(str, str, str), list[Schema]] = schema_repository
        self._exception = exception

    def read_data(
        self, catalog: str, schema: str, table: str, query: str, options: JdbcReaderOptions | None
    ) -> DataFrame | None:
        mock_df = self._dataframe_repository.get((catalog, schema, query))
        if not mock_df:
            return log_and_throw_exception(self._exception, "data", query)
        return mock_df

    def get_schema(self, catalog: str, schema: str, table: str) -> list[Schema] | None:
        mock_schema = self._schema_repository.get((catalog, schema, table))
        if not mock_schema:
            return log_and_throw_exception(self._exception, "schema", table)
        return mock_schema
