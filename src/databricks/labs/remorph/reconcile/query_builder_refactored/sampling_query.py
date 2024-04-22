from pyspark.sql import DataFrame
from sqlglot import parse_one, select
from sqlglot.expressions import Column, Select, union, Expression

from databricks.labs.remorph.reconcile.constants import SampleConfig
from databricks.labs.remorph.reconcile.query_builder_refactored.base import QueryBuilder
from databricks.labs.remorph.reconcile.query_builder_refactored.expression_generator import (
    build_alias,
    build_literal_alias
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
        sql_with_transforms = self._add_transformations(sql)
        query_sql = select(*sql_with_transforms).from_(":tbl").where(self.filter)

        return (
            with_clause.with_(alias="src", as_=query_sql)
            .select("src.*")
            .from_("src")
            .join(expression="recon", join_type="inner", using=key_cols)
            .sql()
        )

    @staticmethod
    def _get_with_clause(df: DataFrame) -> Select:
        union_res = []
        for row in df.take(SampleConfig.sample_rows):
            row_select = [
                build_literal_alias(this=value, alias=col, is_string=False) for col, value in zip(df.columns, row)
            ]
            union_res.append(select(*row_select))
        union_statements = union_concat(union_res, union_res[0], 0)
        return Select().with_(alias='recon', as_=union_statements)

    def _add_transformations(self, sql: str) -> Expression:
        if self.custom_transformations:
            sql_with_custom_transforms = self._apply_custom_transformation(sql).sql(dialect=self.source)
            default_schema = {
                key: self.schema_dict[key] for key in self.schema_dict.keys() if key not in self.custom_transformations
            }
            return self._apply_default_transformation(sql_with_custom_transforms, default_schema)
        return self._apply_default_transformation(sql, self.schema_dict)
