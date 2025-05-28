import logging
from abc import ABC


from databricks.labs.remorph.reconcile.exception import InvalidInputException
from databricks.labs.remorph.reconcile.recon_config import ColumnType, TableMapping, Aggregate, Layer

logger = logging.getLogger(__name__)


class QueryBuilder(ABC):

    _factories: dict[str, type] = {}

    @classmethod
    def for_dialect(cls, table_mapping: TableMapping, column_types: list[ColumnType], layer: Layer, dialect: str):
        factory = cls._factories.get(dialect, None)
        if factory:
            return factory(table_mapping, column_types, layer)
        # default to basic query builder
        return QueryBuilder(table_mapping, column_types, layer)

    def __init__(
        self,
        table_mapping: TableMapping,
        column_types: list[ColumnType],
        layer: Layer,
    ):
        self._table_mapping = table_mapping
        self._column_types = column_types
        self._layer = layer

    @property
    def layer(self) -> Layer:
        return self._layer

    @property
    def column_types(self) -> list[ColumnType]:
        return self._column_types

    @property
    def table_mapping(self) -> TableMapping:
        return self._table_mapping

    @property
    def select_columns(self) -> set[str]:
        return self.table_mapping.get_select_columns(self._column_types, self._layer)

    @property
    def threshold_columns(self) -> set[str]:
        return self.table_mapping.get_threshold_columns(self._layer)

    @property
    def join_columns(self) -> set[str] | None:
        return self.table_mapping.get_join_columns(self._layer)

    @property
    def drop_columns(self) -> set[str]:
        return self._table_mapping.get_drop_columns(self._layer)

    @property
    def partition_column(self) -> set[str]:
        return self._table_mapping.get_partition_column(self._layer)

    @property
    def filter(self) -> str | None:
        return self._table_mapping.get_filter(self._layer)

    @property
    def user_transformations(self) -> dict[str, str]:
        return self._table_mapping.get_transformation_dict(self._layer)

    @property
    def aggregates(self) -> list[Aggregate] | None:
        return self.table_mapping.aggregates

    def _validate(self, field: set[str] | list[str] | None, message: str):
        if field is None:
            message = f"Exception for {self.table_mapping.target_name} target table in {self.layer} layer --> {message}"
            logger.error(message)
            raise InvalidInputException(message)

    def build_count_query(self) -> str:
        where_clause = self._table_mapping.get_filter(self._layer)
        return f"SELECT COUNT(1) AS count FROM :tbl WHERE {where_clause}"
