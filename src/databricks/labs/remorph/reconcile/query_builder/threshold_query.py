import logging

from sqlglot import expressions as exp
from sqlglot import select

from databricks.labs.remorph.reconcile.constants import ThresholdMode
from databricks.labs.remorph.reconcile.query_builder.base import QueryBuilder
from databricks.labs.remorph.reconcile.query_builder.expression_generator import (
    ExpressionGenerator as eg,
)
from databricks.labs.remorph.reconcile.recon_config import TransformRuleMapping
from databricks.labs.remorph.snow.databricks import Databricks

logger = logging.getLogger(__name__)


class ThresholdQueryBuilder(QueryBuilder):
    def build_query(self) -> str:
        all_columns = set(
            self.table_conf.get_threshold_columns
            | self.table_conf.get_join_columns
            | self.table_conf.get_partition_column(self.layer)
        )

        query_columns = sorted(
            all_columns if self.layer == "source" else self._get_mapped_columns(self.src_col_mapping, all_columns)
        )

        transform_rule_mapping = self._get_custom_transformation(
            query_columns, self.transform_dict, self.src_col_mapping
        )
        col_expr = self._get_column_expr(TransformRuleMapping.get_column_expr_with_alias, transform_rule_mapping)

        select_query = self._construct_threshold_query(
            self.table_name, self.table_conf.get_filter(self.layer), col_expr
        )

        return select_query

    @staticmethod
    def _construct_threshold_query(table, query_filter, col_expr) -> str:
        expr = ",".join(col_expr)
        return f"select {expr} from {table} where {query_filter}"

    # Comparison query
    def build_comparison_query(self) -> str:
        select_clause, where = self._generate_select_caluse()
        from_clause, join_clause = self._generate_from_and_join_clause()
        return select(*select_clause).from_(from_clause).join(join_clause).where(where).sql(dialect=Databricks)

    def _generate_select_caluse(self):
        thresholds = self.table_conf.thresholds

        def build_alias(column, table_name):
            return eg().build_alias(this=column, alias=f"{column}_{table_name}", table_name=table_name)

        def build_absolute_case(base, threshold, column):
            return eg().build_alias(eg.build_absolute_case(base=base, threshold=threshold), alias=f"{column}_match")

        select_clause = []
        where_clause = []

        for threshold in thresholds:
            column = threshold.column_name
            source_col = build_alias(column, "source")
            databricks_col = build_alias(column, "databricks")

            base = (
                eg()
                .build_sub(
                    left_column_name=column,
                    left_table_name="source",
                    right_column_name=column,
                    right_table_name="databricks",
                )
                .transform(eg.paran)
                .transform(eg.coalesce)
            )

            if threshold.get_type() == ThresholdMode.NUMBER_ABSOLUTE.value:
                select_clause.append(source_col.transform(eg.coalesce))
                select_clause.append(databricks_col.transform(eg.coalesce))
                select_clause.append(build_absolute_case(base, threshold, column))
                where_clause.append(exp.NEQ(this=base, expression=exp.Literal(this="0", is_string=False)))
            elif threshold.get_type() == ThresholdMode.NUMBER_PERCENTILE.value:
                select_clause.append(source_col.transform(eg.coalesce))
                select_clause.append(databricks_col.transform(eg.coalesce))
                this = eg.build_percentile_case(base=base, threshold=threshold)
                select_clause.append(eg().build_alias(this=this, alias=f"{column}_match"))
                where_clause.append(exp.NEQ(this=base, expression=exp.Literal(this="0", is_string=False)))
            else:
                select_clause.append(source_col.transform(eg.anonymous, "unix_timestamp").transform(eg.coalesce))
                select_clause.append(databricks_col.transform(eg.anonymous, "unix_timestamp").transform(eg.coalesce))
                base = base.transform(eg.anonymous, "unix_timestamp")
                select_clause.append(build_absolute_case(base, threshold, column))
                where_clause.append(exp.NEQ(this=base, expression=exp.Literal(this="0", is_string=False)))

        for column in sorted(self.table_conf.get_join_columns):
            select_clause.append(build_alias(column, "source"))
        where = eg.build_where_clause(where_clause)

        return select_clause, where

    def _generate_from_and_join_clause(self):
        join_columns = sorted(self.table_conf.get_join_columns)
        source_view = f"{self.table_conf.source_name}_df_threshold_vw"
        target_view = f"{self.table_conf.target_name}_df_threshold_vw"

        from_clause = eg.build_from_clause(source_view)
        join_clause = eg.build_join_clause(target_view, join_columns)

        return from_clause, join_clause
