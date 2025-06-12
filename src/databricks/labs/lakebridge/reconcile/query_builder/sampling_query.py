import logging

import sqlglot.expressions as exp
from sqlglot import select
from pyspark.sql import DataFrame

from databricks.labs.lakebridge.reconcile.dialects.utils import get_dialect_name
from databricks.labs.lakebridge.reconcile.query_builder.expression_generator import (
    build_column,
    build_literal,
    _get_is_string,
    build_join_clause,
)
from databricks.labs.lakebridge.reconcile.query_builder.sqlglot_query_builder import SqlglotQueryBuilder
from databricks.labs.lakebridge.reconcile.recon_config import Layer

logger = logging.getLogger(__name__)


def _union_concat(
    unions: list[exp.Select],
    result: exp.Union | exp.Select,
    cnt=0,
) -> exp.Select | exp.Union:
    if len(unions) == 1:
        return result
    if cnt == len(unions) - 2:
        return exp.union(result, unions[cnt + 1])
    cnt = cnt + 1
    res = exp.union(result, unions[cnt])
    return _union_concat(unions, res, cnt)


class SamplingQueryBuilder(SqlglotQueryBuilder):
    def build_query_with_alias(self):
        self._validate(self.join_columns, "Join Columns are compulsory for sampling query")
        join_columns = self.join_columns if self.join_columns else set()

        cols = sorted((join_columns | self.select_columns) - self.threshold_columns - self.drop_columns)

        cols_with_alias = [
            build_column(this=col, alias=self.table_mapping.get_layer_tgt_to_src_col_mapping(col, self.layer))
            for col in cols
        ]

        query = select(*cols_with_alias).from_(":tbl").where(self.filter).sql(dialect=self._dialect)

        logger.info(f"Sampling Query with Alias for {self.layer}: {query}")
        return query

    def build_query(self, df: DataFrame):
        self._validate(self.join_columns, "Join Columns are compulsory for sampling query")
        join_columns = self.join_columns if self.join_columns else set()
        if self.layer is Layer.SOURCE:
            key_cols = sorted(join_columns)
        else:
            key_cols = sorted(self.table_mapping.get_tgt_to_src_col_mapping_list(join_columns))
        keys_df = df.select(*key_cols)
        with_clause = self._get_with_clause(keys_df)

        cols = sorted((join_columns | self.select_columns) - self.threshold_columns - self.drop_columns)

        cols_with_alias = [
            build_column(this=col, alias=self.table_mapping.get_layer_tgt_to_src_col_mapping(col, self.layer))
            for col in cols
        ]

        sql_with_transforms = self.add_transformations(cols_with_alias, self._dialect)
        query_sql = select(*sql_with_transforms).from_(":tbl").where(self.filter)
        if self.layer is Layer.SOURCE:
            with_select = [build_column(this=col, table_name="src") for col in sorted(cols)]
        else:
            with_select = [
                build_column(this=col, table_name="src")
                for col in sorted(self.table_mapping.get_tgt_to_src_col_mapping_list(cols))
            ]

        join_clause = SamplingQueryBuilder._get_join_clause(key_cols)

        query = (
            with_clause.with_(alias="src", as_=query_sql)
            .select(*with_select)
            .from_("src")
            .join(join_clause)
            .sql(dialect=self._dialect)
        )
        logger.info(f"Sampling Query for {self.layer}: {query}")
        return query

    @classmethod
    def _get_join_clause(cls, key_cols: list):
        return build_join_clause(
            "recon", key_cols, source_table_alias="src", target_table_alias="recon", kind="inner", func=exp.EQ
        )

    def _get_with_clause(self, df: DataFrame) -> exp.Select:
        union_res = []
        for row in df.collect():
            column_types = [(str(f.name).lower(), f.dataType) for f in df.schema.fields]
            column_types_dict = dict(column_types)
            orig_types_dict = {
                schema.column_name: schema.data_type
                for schema in self.column_types
                if schema.column_name not in self.user_transformations
            }
            row_select = [
                (
                    build_literal(
                        this=str(value),
                        alias=col,
                        is_string=_get_is_string(column_types_dict, col),
                        cast=orig_types_dict.get(col),
                    )
                    if value is not None
                    else exp.Alias(this=exp.Null(), alias=col)
                )
                for col, value in zip(df.columns, row)
            ]
            if get_dialect_name(self._dialect) == "oracle":
                union_res.append(select(*row_select).from_("dual"))
            else:
                union_res.append(select(*row_select))
        union_statements = _union_concat(union_res, union_res[0], 0)
        return exp.Select().with_(alias='recon', as_=union_statements)
