from sqlglot import Dialect, Expression, parse_one
from sqlglot.expressions import Column

from databricks.labs.lakebridge.reconcile.dialects.utils import get_dialect_name, get_dialect
from databricks.labs.lakebridge.reconcile.query_builder.expression_generator import (
    DataType_transform_mapping,
    transform_expression,
)
from databricks.labs.lakebridge.reconcile.query_builder.query_builder import QueryBuilder
from databricks.labs.lakebridge.reconcile.recon_config import ColumnType, Layer, TableMapping


class SqlglotQueryBuilder(QueryBuilder):

    @staticmethod
    def _default_transformer(node: Expression, column_types: list[ColumnType], dialect: Dialect) -> Expression:

        def _get_transform(datatype: str):
            dialect_name = get_dialect_name(dialect)
            source_mapping = DataType_transform_mapping.get(dialect_name, {})

            if source_mapping.get(datatype.upper()) is not None:
                return source_mapping.get(datatype.upper())
            if source_mapping.get("default") is not None:
                return source_mapping.get("default")

            return DataType_transform_mapping.get("universal", {}).get("default")

        schema_dict = {v.column_name: v.data_type for v in column_types}
        if isinstance(node, Column):
            column_name = node.name
            if column_name in schema_dict.keys():
                transform = _get_transform(schema_dict.get(column_name, column_name))
                return transform_expression(node, transform)
        return node

    def __init__(self, table_mapping: TableMapping, column_types: list[ColumnType], layer: Layer, dialect: Dialect):
        super().__init__(table_mapping, column_types, layer)
        self._dialect = dialect
        self._user_transformations = None

    def sqlglot_apply_transformations(self, aliases: list[Expression], source: Dialect) -> list[Expression]:
        if self._user_transformations:
            alias_with_user_transforms = self._sqlglot_apply_user_transformations(aliases)
            default_transform_column_types: list[ColumnType] = list(
                filter(lambda sch: sch.column_name not in self._user_transformations.keys(), self.column_types)
            )
            return self._sqlglot_apply_default_transformer(
                alias_with_user_transforms, default_transform_column_types, source
            )
        return self._sqlglot_apply_default_transformer(aliases, self.column_types, source)

    def _sqlglot_apply_transformations(self, node: Expression, transformations: dict[str, str]) -> Expression:
        if not transformations or not isinstance(node, Column):
            return node
        column_name = node.name
        if column_name in transformations.keys():
            dialect = self._dialect if self.layer is Layer.SOURCE else get_dialect("databricks")
            return parse_one(transformations.get(column_name, column_name), read=dialect)
        return node

    def _sqlglot_apply_user_transformations(self, aliases: list[Expression]):
        return list(
            alias.transform(self._sqlglot_apply_transformations, self._user_transformations) for alias in aliases
        )

    def _sqlglot_apply_default_transformer(
        self, aliases: list[Expression], column_types: list[ColumnType], source: Dialect
    ) -> list[Expression]:
        return list(alias.transform(self._default_transformer, column_types, source) for alias in aliases)
