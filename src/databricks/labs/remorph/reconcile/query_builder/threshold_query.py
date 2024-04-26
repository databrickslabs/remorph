import logging

from sqlglot import expressions as exp
from sqlglot import select

from databricks.labs.remorph.reconcile.constants import ThresholdMode
from databricks.labs.remorph.reconcile.query_builder.base import QueryBuilder
from databricks.labs.remorph.reconcile.query_builder.expression_generator import (
    anonymous,
    build_column,
    build_from_clause,
    build_join_clause,
    build_sub,
    build_threshold_absolute_case,
    build_threshold_percentage_case,
    build_where_clause,
    coalesce,
)
from databricks.labs.remorph.reconcile.recon_config import Thresholds
from databricks.labs.remorph.snow.databricks import Databricks

logger = logging.getLogger(__name__)


class ThresholdQueryBuilder(QueryBuilder):
    # Comparison query
    def build_comparison_query(self) -> str:
        select_clause, where = self._generate_select_where_clause()
        from_clause, join_clause = self._generate_from_and_join_clause()
        # for threshold comparison query the dialect is always Daabricks
        query = select(*select_clause).from_(from_clause).join(join_clause).where(where).sql(dialect=Databricks)
        logger.info(f"Threshold Comparison query: {query}")
        return query

    def _generate_select_where_clause(self) -> tuple[list[exp.Alias], exp.Or]:
        thresholds = self.table_conf.thresholds

        def _build_alias(this: str, table_name: str):
            return build_column(this=this, alias=f"{this}_{table_name}", table_name=table_name)

        def _build_absolute_case(base: exp.Expression, threshold: Thresholds, column: str):
            return build_column(
                this=build_threshold_absolute_case(base=base, threshold=threshold), alias=f"{column}_match"
            )

        select_clause = []
        where_clause = []

        for threshold in thresholds:
            column = threshold.column_name
            source_col = _build_alias(column, "source")
            databricks_col = _build_alias(column, "databricks")

            base = exp.Paren(
                this=build_sub(
                    left_column_name=column,
                    left_table_name="source",
                    right_column_name=column,
                    right_table_name="databricks",
                )
            ).transform(coalesce)

            if threshold.get_type() == ThresholdMode.NUMBER_ABSOLUTE.value:
                select_clause.append(source_col.transform(coalesce))
                select_clause.append(databricks_col.transform(coalesce))
                select_clause.append(_build_absolute_case(base, threshold, column))
                where_clause.append(exp.NEQ(this=base, expression=exp.Literal(this="0", is_string=False)))
            elif threshold.get_type() == ThresholdMode.NUMBER_PERCENTILE.value:
                select_clause.append(source_col.transform(coalesce))
                select_clause.append(databricks_col.transform(coalesce))
                this = build_threshold_percentage_case(base=base, threshold=threshold)
                select_clause.append(build_column(this=this, alias=f"{column}_match"))
                where_clause.append(exp.NEQ(this=base, expression=exp.Literal(this="0", is_string=False)))
            else:
                select_clause.append(source_col.transform(anonymous, "unix_timestamp({})").transform(coalesce))
                select_clause.append(databricks_col.transform(anonymous, "unix_timestamp({})").transform(coalesce))
                exp_anonymous = base.transform(anonymous, "unix_timestamp({})")
                select_clause.append(_build_absolute_case(exp_anonymous, threshold, column))
                where_clause.append(exp.NEQ(this=exp_anonymous, expression=exp.Literal(this="0", is_string=False)))

        for column in sorted(self.table_conf.get_join_columns("source")):
            select_clause.append(_build_alias(column, "source"))
        where = build_where_clause(where_clause)

        return select_clause, where

    def _generate_from_and_join_clause(self) -> tuple[exp.From, exp.Join]:
        join_columns = sorted(self.table_conf.get_join_columns("source"))
        source_view = f"{self.table_conf.source_name}_df_threshold_vw"
        target_view = f"{self.table_conf.target_name}_df_threshold_vw"

        from_clause = build_from_clause(source_view, "source")
        join_clause = build_join_clause(table_name=target_view, table_alias="databricks", join_columns=join_columns)

        return from_clause, join_clause
