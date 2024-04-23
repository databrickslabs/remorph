from abc import ABC

from sqlglot import parse_one
from sqlglot.expressions import Alias, Column, Expression

from databricks.labs.remorph.reconcile.query_builder_refactored.expression_generator import (
    DataType_transform_mapping,
    transform_expression,
)
from databricks.labs.remorph.reconcile.query_builder_refactored.recon_config import (
    Schema,
    Table,
)


class QueryBuilder(ABC):

    def __init__(self, table_conf: Table, schema: list[Schema], layer: str, source: str):
        self._table_conf = table_conf
        self._schema = schema
        self._layer = layer
        self._source = source

    @property
    def source(self) -> str:
        return self._source

    @property
    def layer(self) -> str:
        return self._layer

    @property
    def table_conf(self) -> Table:
        return self._table_conf

    @property
    def schema_dict(self) -> dict[str, str]:
        return {v.column_name: v.data_type for v in self._schema}

    @property
    def select_columns(self) -> set[str]:
        return self.table_conf.get_select_columns(self._schema, self._layer)

    @property
    def threshold_columns(self) -> set[str]:
        return self.table_conf.get_threshold_columns(self._layer)

    @property
    def join_columns(self) -> set[str]:
        return self.table_conf.get_join_columns(self._layer)

    @property
    def drop_columns(self) -> set[str]:
        return self._table_conf.get_drop_columns(self._layer)

    @property
    def partition_column(self) -> set[str]:
        return self._table_conf.get_partition_column(self._layer)

    @property
    def filter(self) -> str | None:
        return self._table_conf.get_filter(self._layer)

    @property
    def custom_transformations(self) -> dict[str, str]:
        return self._table_conf.get_transformation_dict(self._layer)

    @property
    def table_name(self) -> str:
        return self._table_conf.source_name if self._layer == "source" else self._table_conf.target_name

    def apply_custom_transformation(self, aliases: list[Alias]) -> list[Alias]:
        with_transform = []
        for alias in aliases:
            with_transform.append(alias.transform(self._custom_transformer, self.custom_transformations))
        return with_transform

    @staticmethod
    def _custom_transformer(node: Expression, custom_transformations: dict[str, str]) -> Expression:
        if isinstance(node, Column) and custom_transformations:
            column_name = node.name
            if column_name in custom_transformations.keys():
                return parse_one(custom_transformations.get(column_name))
        return node

    def apply_default_transformation(self, aliases: list[Alias], schema: dict[str, str]) -> list[Alias]:
        with_transform = []
        for alias in aliases:
            with_transform.append(alias.transform(self._default_transformer, schema))
        return with_transform

    @staticmethod
    def _default_transformer(node: Expression, schema: dict[str, str]) -> Expression:
        if isinstance(node, Column):
            column_name = node.name
            if column_name in schema.keys():
                return transform_expression(node, DataType_transform_mapping.get(schema.get(column_name).upper()))
        return node
