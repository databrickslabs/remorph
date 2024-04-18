from pyspark.sql import DataFrame
from sqlglot import parse_one, select
from sqlglot.expressions import Column

from databricks.labs.remorph.reconcile.query_builder_refactored.base import QueryBuilder
from databricks.labs.remorph.reconcile.query_builder_refactored.expression_generator import (
    build_alias,
    default_transformer,
)


class SamplingQueryBuilder(QueryBuilder):

    def build_query(self, df: DataFrame):
        # key_cols = sorted(self.join_columns)
        # keys_df = df.select(*key_cols)
        # with_clause = self._get_with_clause(keys_df, self.source)

        cols = sorted((self.join_columns | self.select_columns) - self.threshold_columns - self.drop_columns)

        col_with_alias = [build_alias(this=col, alias=self.table_conf.get_col_mapping(col, self.layer)) for col in cols]

        sql = select(*col_with_alias).sql()
        if self.custom_transformations:
            default_schema = {
                key: self.schema_dict[key] for key in self.schema_dict.keys() if key not in self.custom_transformations
            }
            sql_with_default_transforms = self._apply_default_transformation(sql, default_schema, self.source)
            sql_with_all_transforms = self._apply_custom_transformation(sql_with_default_transforms)
        else:
            sql_with_all_transforms = self._apply_default_transformation(sql, self.schema_dict, self.source)
        return sql_with_all_transforms

    def _apply_custom_transformation(self, sql):
        return parse_one(sql).transform(self._custom_transformer, self.custom_transformations)

    @staticmethod
    def _custom_transformer(node, custom_transformations: dict[str, str]):
        if isinstance(node, Column) and custom_transformations:
            column_name = node.name
            if column_name in custom_transformations.keys():
                return parse_one(custom_transformations.get(column_name))
        return node

    @staticmethod
    def _apply_default_transformation(sql: str, schema: dict[str, str], dialect: str):
        return parse_one(sql).transform(default_transformer, schema).sql(dialect)
