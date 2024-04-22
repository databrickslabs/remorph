from pyspark.sql import DataFrame
from sqlglot import parse_one, select
from sqlglot.expressions import Column, Select, union

from databricks.labs.remorph.reconcile.query_builder_refactored.base import QueryBuilder
from databricks.labs.remorph.reconcile.query_builder_refactored.expression_generator import (
    build_alias,
    build_literal_alias,
    default_transformer,
)


def union_concat(unions, result, cnt=0):
    if len(unions) == 1:
        return result
    if cnt == len(unions) - 2:
        return union(result, unions[cnt + 1])
    cnt = cnt + 1
    res = union(result, unions[cnt])
    return union_concat(unions, res, cnt)


class SamplingQueryBuilder(QueryBuilder):

    def build_query(self, df: DataFrame):
        if self.layer == "source":
            key_cols = sorted(self.join_columns)
        else:
            key_cols = sorted(self.table_conf.get_tgt_to_src_col_mapping(self.join_columns, self.layer))
        keys_df = df.select(*key_cols)
        with_clause = self._get_with_clause(keys_df)

        cols = sorted((self.join_columns | self.select_columns) - self.threshold_columns - self.drop_columns)

        col_with_alias = [
            build_alias(this=col, alias=self.table_conf.get_tgt_to_src_col_mapping(col, self.layer)) for col in cols
        ]

        sql = select(*col_with_alias).sql()
        if self.custom_transformations:
            default_schema = {
                key: self.schema_dict[key] for key in self.schema_dict.keys() if key not in self.custom_transformations
            }
            sql_with_default_transforms = self._apply_default_transformation(sql, default_schema)
            sql_with_all_transforms = self._apply_custom_transformation(sql_with_default_transforms)
        else:
            sql_with_all_transforms = self._apply_default_transformation(sql, self.schema_dict)
        query_sql = select(*sql_with_all_transforms).from_(":tbl")

        return (
            with_clause.with_(alias="src", as_=query_sql)
            .select("src.*")
            .from_("src")
            .join(expression="recon", join_type="inner", using=key_cols)
        )

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
    def _apply_default_transformation(sql: str, schema: dict[str, str]):
        return parse_one(sql).transform(default_transformer, schema)

    @staticmethod
    def _get_with_clause(df):
        union_res = []
        for row in df.take(50):
            row_select = [
                build_literal_alias(this=value, alias=col, is_string=False) for col, value in zip(df.columns, row)
            ]
            union_res.append(select(*row_select))
        union_statements = union_concat(union_res, union_res[0], 0)
        return Select().with_(alias='recon', as_=union_statements)
