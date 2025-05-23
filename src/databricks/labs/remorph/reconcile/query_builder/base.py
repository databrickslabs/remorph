import logging
from abc import ABC

import sqlglot.expressions as exp
from sqlglot import Dialect, parse_one

from databricks.labs.remorph.reconcile.dialects.utils import get_dialect, get_dialect_name
from databricks.labs.remorph.reconcile.exception import InvalidInputException
from databricks.labs.remorph.reconcile.query_builder.expression_generator import (
    DataType_transform_mapping,
    transform_expression,
)
from databricks.labs.remorph.reconcile.recon_config import ColumnType, TableMapping, Aggregate, Layer

logger = logging.getLogger(__name__)


class QueryBuilder(ABC):
    def __init__(
        self,
        table_mapping: TableMapping,
        column_types: list[ColumnType],
        layer: Layer,
        dialect: Dialect,
    ):
        self._table_mapping = table_mapping
        self._column_types = column_types
        self._layer = layer
        self._dialect = dialect

    @property
    def dialect(self) -> Dialect:
        return self._dialect

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

    def add_transformations(self, aliases: list[exp.Expression], source: Dialect) -> list[exp.Expression]:
        if self.user_transformations:
            alias_with_user_transforms = self._apply_user_transformation(aliases)
            default_transform_column_types: list[ColumnType] = list(
                filter(lambda sch: sch.column_name not in self.user_transformations.keys(), self.column_types)
            )
            return self._apply_default_transformation(
                alias_with_user_transforms, default_transform_column_types, source
            )
        return self._apply_default_transformation(aliases, self.column_types, source)

    def _apply_user_transformation(self, aliases: list[exp.Expression]) -> list[exp.Expression]:
        with_transform = []
        for alias in aliases:
            with_transform.append(alias.transform(self._user_transformer, self.user_transformations))
        return with_transform

    def _user_transformer(self, node: exp.Expression, user_transformations: dict[str, str]) -> exp.Expression:
        if isinstance(node, exp.Column) and user_transformations:
            dialect = self._dialect if self.layer is Layer.SOURCE else get_dialect("databricks")
            column_name = node.name
            if column_name in user_transformations.keys():
                return parse_one(user_transformations.get(column_name, column_name), read=dialect)
        return node

    def _apply_default_transformation(
        self, aliases: list[exp.Expression], column_types: list[ColumnType], source: Dialect
    ) -> list[exp.Expression]:
        with_transform = []
        for alias in aliases:
            with_transform.append(alias.transform(self._default_transformer, column_types, source))
        return with_transform

    @staticmethod
    def _default_transformer(node: exp.Expression, column_types: list[ColumnType], dialect: Dialect) -> exp.Expression:

        def _get_transform(datatype: str):
            dialect_name = get_dialect_name(dialect)
            source_mapping = DataType_transform_mapping.get(dialect_name, {})

            if source_mapping.get(datatype.upper()) is not None:
                return source_mapping.get(datatype.upper())
            if source_mapping.get("default") is not None:
                return source_mapping.get("default")

            return DataType_transform_mapping.get("universal", {}).get("default")

        schema_dict = {v.column_name: v.data_type for v in column_types}
        if isinstance(node, exp.Column):
            column_name = node.name
            if column_name in schema_dict.keys():
                transform = _get_transform(schema_dict.get(column_name, column_name))
                return transform_expression(node, transform)
        return node

    def _validate(self, field: set[str] | list[str] | None, message: str):
        if field is None:
            message = f"Exception for {self.table_mapping.target_name} target table in {self.layer} layer --> {message}"
            logger.error(message)
            raise InvalidInputException(message)
