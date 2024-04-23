from pyspark.sql import DataFrame
from sqlglot import select
from sqlglot.expressions import Alias, Select, union

from databricks.labs.remorph.reconcile.constants import SampleConfig
from databricks.labs.remorph.reconcile.query_builder_refactored.base import QueryBuilder
from databricks.labs.remorph.reconcile.query_builder_refactored.expression_generator import (
    build_column,
    build_literal,
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

        cols_with_alias = [
            build_column(this=col, alias=self.table_conf.get_tgt_to_src_col_mapping(col, self.layer)) for col in cols
        ]

        sql_with_transforms = self._add_transformations(cols_with_alias)
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
        for row in df.take(SampleConfig.SAMPLE_ROWS):
            row_select = [build_literal(this=value, alias=col, is_string=False) for col, value in zip(df.columns, row)]
            union_res.append(select(*row_select))
        union_statements = union_concat(union_res, union_res[0], 0)
        return Select().with_(alias='recon', as_=union_statements)

    def _add_transformations(self, aliases: list[Alias]) -> list[Alias]:
        if self.custom_transformations:
            alias_with_custom_transforms = self.apply_custom_transformation(aliases)
            default_schema = {
                key: self.schema_dict[key] for key in self.schema_dict.keys() if key not in self.custom_transformations
            }
            return self.apply_default_transformation(alias_with_custom_transforms, default_schema)
        return self.apply_default_transformation(aliases, self.schema_dict)
