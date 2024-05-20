import sqlglot.expressions as exp
from pyspark.sql import DataFrame
from sqlglot import select

from databricks.labs.remorph.reconcile.query_builder.base import QueryBuilder
from databricks.labs.remorph.reconcile.query_builder.expression_generator import (
    build_column,
    build_literal,
)

_SAMPLE_ROWS = 50


def _union_concat(unions: list[exp.Select], result: exp.Union | exp.Select, cnt=0) -> exp.Select | exp.Union:
    if len(unions) == 1:
        return result
    if cnt == len(unions) - 2:
        return exp.union(result, unions[cnt + 1])
    cnt = cnt + 1
    res = exp.union(result, unions[cnt])
    return _union_concat(unions, res, cnt)


class SamplingQueryBuilder(QueryBuilder):
    def build_query(self, df: DataFrame):
        if self.layer == "source":
            key_cols = sorted(self.join_columns)
        else:
            key_cols = sorted(self.table_conf.get_tgt_to_src_col_mapping(self.join_columns, self.layer))
        keys_df = df.select(*key_cols)
        with_clause = self._get_with_clause(keys_df)

        cols = sorted((self.join_columns | self.select_columns) - self.threshold_columns - self.drop_columns)

        cols_with_alias = [
            build_column(this=col, alias=self.table_conf.get_tgt_to_src_col_mapping(col, self.layer)) for col in cols
        ]

        sql_with_transforms = self.add_transformations(cols_with_alias, self.source)
        query_sql = select(*sql_with_transforms).from_(":tbl").where(self.filter)
        with_select = sorted(self.table_conf.get_tgt_to_src_col_mapping(cols, self.layer))

        return (
            with_clause.with_(alias="src", as_=query_sql)
            .select(*with_select)
            .from_("src")
            .join(expression="recon", join_type="inner", using=key_cols)
            .sql(dialect=self.source)
        )

    @staticmethod
    def _get_with_clause(df: DataFrame) -> exp.Select:
        union_res = []
        for row in df.take(_SAMPLE_ROWS):
            row_select = [build_literal(this=value, alias=col, is_string=False) for col, value in zip(df.columns, row)]
            union_res.append(select(*row_select))
        union_statements = _union_concat(union_res, union_res[0], 0)
        return exp.Select().with_(alias='recon', as_=union_statements)
