import logging
from abc import ABC, abstractmethod

from pyspark.sql import DataFrame

from databricks.labs.remorph.config import TableRecon
from databricks.labs.remorph.reconcile.exception import DataSourceRuntimeException
from databricks.labs.remorph.reconcile.recon_config import JdbcReaderOptions, Schema, Table

logger = logging.getLogger(__name__)


def get_where_condition(
    include_list: list[str] | None,
    exclude_list: list[str] | None,
) -> str:
    filter_list = None
    in_clause = None

    if include_list:
        filter_list = include_list
        in_clause = "IN"

    if exclude_list:
        filter_list = exclude_list
        in_clause = "NOT IN"

    where_cond = ""
    if filter_list:
        subset_tables = ", ".join(filter_list)
        where_cond = f"AND TABLE_NAME {in_clause} ({subset_tables})"

    return where_cond


def build_table_recon(
    catalog: str | None,
    schema: str,
    tables_list: list[Table],
) -> TableRecon:
    return TableRecon(
        source_catalog=catalog,
        source_schema=schema,
        target_catalog="",
        target_schema="",
        tables=tables_list,
    )


class DataSource(ABC):
    @abstractmethod
    def read_data(
        self,
        catalog: str | None,
        schema: str,
        table: str,
        query: str,
        options: JdbcReaderOptions | None,
    ) -> DataFrame:
        return NotImplemented

    @abstractmethod
    def get_schema(
        self,
        catalog: str | None,
        schema: str,
        table: str,
    ) -> list[Schema]:
        return NotImplemented

    @abstractmethod
    def list_tables(
        self,
        catalog: str | None,
        schema: str,
        include_list: list[str] | None,
        exclude_list: list[str] | None,
    ) -> TableRecon:
        return NotImplemented

    @classmethod
    def log_and_throw_exception(cls, exception: Exception, fetch_type: str, query: str):
        error_msg = f"Runtime exception occurred while fetching {fetch_type} using {query} : {exception}"
        logger.warning(error_msg)
        raise DataSourceRuntimeException(error_msg) from exception


class MockDataSource(DataSource):

    def __init__(
        self,
        dataframe_repository: dict[tuple[str, str, str], DataFrame],
        schema_repository: dict[tuple[str, str, str], list[Schema]],
        exception: Exception = RuntimeError("Mock Exception"),
    ):
        self._dataframe_repository: dict[tuple[str, str, str], DataFrame] = dataframe_repository
        self._schema_repository: dict[tuple[str, str, str], list[Schema]] = schema_repository
        self._exception = exception

    def read_data(
        self,
        catalog: str | None,
        schema: str,
        table: str,
        query: str,
        options: JdbcReaderOptions | None,
    ) -> DataFrame:
        catalog_str = catalog if catalog else ""
        mock_df = self._dataframe_repository.get((catalog_str, schema, query))
        if not mock_df:
            return self.log_and_throw_exception(self._exception, "data", f"({catalog}, {schema}, {query})")
        return mock_df

    def get_schema(self, catalog: str | None, schema: str, table: str) -> list[Schema]:
        catalog_str = catalog if catalog else ""
        mock_schema = self._schema_repository.get((catalog_str, schema, table))
        if not mock_schema:
            return self.log_and_throw_exception(self._exception, "schema", f"({catalog}, {schema}, {table})")
        return mock_schema

    def list_tables(
        self,
        catalog: str | None,
        schema: str,
        include_list: list[str] | None,
        exclude_list: list[str] | None,
    ) -> TableRecon:
        raise NotImplementedError("list_tables method is not implemented for DataSource")
