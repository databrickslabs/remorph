import sqlglot.expressions as exp

from databricks.labs.remorph.reconcile.query_builder.base import QueryBuilder
from databricks.labs.remorph.reconcile.query_builder.expression_generator import (
    build_column,
    concat,
    get_hash_transform,
    lower,
    transform_expression,
)
from databricks.labs.remorph.reconcile.recon_config import Schema


class HashQueryBuilder(QueryBuilder):
    def build_query(self) -> str:
        hash_cols = sorted((self.join_columns | self.select_columns) - self.threshold_columns - self.drop_columns)
        key_cols = sorted(self.join_columns | self.partition_column)

        cols_with_alias = [
            build_column(this=col, alias=self.table_conf.get_tgt_to_src_col_mapping(col, self.layer))
            for col in key_cols
        ]

        key_cols_with_transform = self._add_transformations(cols_with_alias, self.source)
        hash_col_with_transform = [self._generate_hash_algorithm(hash_cols)]

        res = exp.select(*hash_col_with_transform + key_cols_with_transform).from_(":tbl").where(self.filter).sql()

        return res

    def _add_transformations(self, aliases: list[exp.Alias], source: str) -> list[exp.Alias]:
        if self.user_transformations:
            alias_with_user_transforms = self.apply_user_transformation(aliases)
            default_transform_schema: list[Schema] = list(
                filter(lambda sch: sch.column_name not in self.user_transformations.keys(), self.schema)
            )
            return self.apply_default_transformation(alias_with_user_transforms, default_transform_schema, source)
        return self.apply_default_transformation(aliases, self.schema, source)

    def _generate_hash_algorithm(self, cols: list[str]) -> exp.Expression:
        cols_with_alias = [build_column(this=col, alias=None) for col in cols]
        cols_with_transform = self._add_transformations(cols_with_alias, self.source)
        col_exprs = exp.select(*cols_with_transform).iter_expressions()
        concat_expr = concat(list(col_exprs))

        hash_expr = concat_expr.transform(self._hash_transform, self.source).transform(lower, is_expr=True)

        return build_column(hash_expr, alias="hash_value_recon")

    @staticmethod
    def _hash_transform(node: exp.Expression, source: str):
        transform = get_hash_transform(source)
        return transform_expression(node, transform)
