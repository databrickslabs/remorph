import logging

import sqlglot.expressions as exp
from pyspark.sql import DataFrame
from sqlglot import select

from databricks.labs.remorph.config import get_key_from_dialect
from databricks.labs.remorph.reconcile.query_builder.base import QueryBuilder
from databricks.labs.remorph.reconcile.query_builder.expression_generator import (
    build_column,
    build_literal,
    _get_is_string,
    build_join_clause,
    trim,
    coalesce,
)

_SAMPLE_ROWS = 50

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


class TsqlSamplingQueryBuilder(QueryBuilder):
    def build_query(self, df: DataFrame):
        self._validate(self.join_columns, "Join Columns are compulsory for sampling query")
        join_columns = self.join_columns if self.join_columns else set()
        if self.layer == "source":
            key_cols = sorted(join_columns)
        else:
            key_cols = sorted(self.table_conf.get_tgt_to_src_col_mapping_list(join_columns))

        # Build the `src` subquery
        cols = sorted((join_columns | self.select_columns) - self.threshold_columns - self.drop_columns)
        cols_with_alias = [
            build_column(this=col, alias=self.table_conf.get_layer_tgt_to_src_col_mapping(col, self.layer))
            for col in cols
        ]
        sql_with_transforms = self.add_transformations(cols_with_alias, self.engine)
        src_subquery = select(*sql_with_transforms).from_(":tbl").where(self.filter).sql(dialect=self.engine)
        src_subquery_sql = f"({src_subquery}) AS src"

        # Build the `recon` subquery
        union_res = []
        for row in df.take(_SAMPLE_ROWS):
            column_types = [(str(f.name).lower(), f.dataType) for f in df.schema.fields]
            column_types_dict = dict(column_types)
            row_select = [
                (
                    build_literal(this=str(value), alias=col, is_string=_get_is_string(column_types_dict, col))
                    if value is not None
                    else exp.Alias(this=exp.Null(), alias=col)
                )
                for col, value in zip(df.columns, row)
            ]
            if get_key_from_dialect(self.engine) == "oracle":
                union_res.append(select(*row_select).from_("dual"))
            else:
                union_res.append(select(*row_select))
        union_statements = _union_concat(union_res, union_res[0], 0)
        recon_subquery = f"({union_statements.sql(dialect=self.engine)}) AS recon"

        # Build the join condition manually, handling string columns with TRIM
        column_types = [(str(f.name).lower(), f.dataType) for f in df.schema.fields]
        column_types_dict = dict(column_types)

        join_condition = ' AND '.join(
            [
                (
                    f"COALESCE(LTRIM(RTRIM(src.{col})), '_null_recon_') = COALESCE(LTRIM(RTRIM(recon.{col})), '_null_recon_')"
                    if _get_is_string(column_types_dict, col)
                    else f"COALESCE(src.{col}, '_null_recon_') = COALESCE(recon.{col}, '_null_recon_')"
                )
                for col in key_cols
            ]
        )
        # regex replace

        # Manually construct the final query
        final_query = f"""
        SELECT src.{', src.'.join(cols)}
        FROM {src_subquery_sql}
        INNER JOIN {recon_subquery}
        ON {join_condition}
        """

        logger.info(f"Sampling Query for {self.layer}: {final_query}")
        return final_query

    @classmethod
    def _get_join_clause(cls, key_cols: list):
        # Not used in this version, kept for reference
        return (
            build_join_clause(
                "recon", key_cols, source_table_alias="src", target_table_alias="recon", kind="inner", func=exp.EQ
            )
            .transform(coalesce, default="_null_recon_", is_string=True)
            .transform(trim)
        )

    def _get_with_clause(self, df: DataFrame) -> exp.Select:
        union_res = []
        for row in df.take(_SAMPLE_ROWS):
            column_types = [(str(f.name).lower(), f.dataType) for f in df.schema.fields]
            column_types_dict = dict(column_types)
            row_select = [
                (
                    build_literal(this=str(value), alias=col, is_string=_get_is_string(column_types_dict, col))
                    if value is not None
                    else exp.Alias(this=exp.Null(), alias=col)
                )
                for col, value in zip(df.columns, row)
            ]
            if get_key_from_dialect(self.engine) == "oracle":
                union_res.append(select(*row_select).from_("dual"))
            else:
                union_res.append(select(*row_select))
        union_statements = _union_concat(union_res, union_res[0], 0)
        return exp.Select().with_(alias='recon', as_=union_statements)
