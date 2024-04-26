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
        select_clause = []
        where_clause = []

        for threshold in thresholds:
            column = threshold.column_name
            base = exp.Paren(
                this=build_sub(
                    left_column_name=column,
                    left_table_name="source",
                    right_column_name=column,
                    right_table_name="databricks",
                )
            ).transform(coalesce)

            if threshold.get_type() == ThresholdMode.NUMBER_ABSOLUTE.value:
                select_exp, where = self._build_expression_numeric_absolute(threshold, base)
                select_clause.extend(select_exp)
                where_clause.append(where)
            elif threshold.get_type() == ThresholdMode.NUMBER_PERCENTAGE.value:
                select_exp, where = self._build_expression_numeric_percentage(threshold, base)
                select_clause.extend(select_exp)
                where_clause.append(where)
            else:
                select_exp, where = self._build_expression_datetime(threshold, base)
                select_clause.extend(select_exp)
                where_clause.append(where)

        for column in sorted(self.table_conf.get_join_columns("source")):
            select_clause.append(build_column(this=column, alias=f"{column}_source", table_name="source"))
        where = build_where_clause(where_clause)

        return select_clause, where

    def _build_expression_alias_components(
        self, threshold: Thresholds, base: exp.Expression
    ) -> tuple[list[exp.Alias], exp.Expression]:
        select_clause = []
        column = threshold.column_name
        select_clause.append(
            build_column(this=column, alias=f"{column}_source", table_name="source").transform(coalesce)
        )
        select_clause.append(
            build_column(this=column, alias=f"{column}_databricks", table_name="databricks").transform(coalesce)
        )
        where = exp.NEQ(this=base, expression=exp.Literal(this="0", is_string=False))
        return select_clause, where

    def _build_expression_numeric_absolute(
        self, threshold: Thresholds, base: exp.Expression
    ) -> tuple[list[exp.Alias], exp.Expression]:
        column = threshold.column_name
        select_clause, where = self._build_expression_alias_components(threshold, base)
        select_clause.append(
            build_column(
                this=self._build_threshold_absolute_case(base=base, threshold=threshold), alias=f"{column}_match"
            )
        )
        return select_clause, where

    def _build_expression_numeric_percentage(
        self, threshold: Thresholds, base: exp.Expression
    ) -> tuple[list[exp.Alias], exp.Expression]:
        column = threshold.column_name
        select_clause, where = self._build_expression_alias_components(threshold, base)
        select_clause.append(
            build_column(
                this=self._build_threshold_percentage_case(base=base, threshold=threshold), alias=f"{column}_match"
            )
        )
        return select_clause, where

    def _build_expression_datetime(
        self, threshold: Thresholds, base: exp.Expression
    ) -> tuple[list[exp.Alias], exp.Expression]:
        select_clause = []
        column = threshold.column_name
        select_clause, _ = self._build_expression_alias_components(threshold, base)
        select_clause = [expression.transform(anonymous, "unix_timestamp({})") for expression in select_clause]
        exp_anonymous = base.transform(anonymous, "unix_timestamp({})")
        select_clause.append(
            build_column(
                this=self._build_threshold_absolute_case(base=exp_anonymous, threshold=threshold),
                alias=f"{column}_match",
            )
        )
        where = exp.NEQ(this=exp_anonymous, expression=exp.Literal(this="0", is_string=False))
        return select_clause, where

    def _generate_from_and_join_clause(self) -> tuple[exp.From, exp.Join]:
        join_columns = sorted(self.table_conf.get_join_columns("source"))
        source_view = f"{self.table_conf.source_name}_df_threshold_vw"
        target_view = f"{self.table_conf.target_name}_df_threshold_vw"

        from_clause = build_from_clause(source_view, "source")
        join_clause = build_join_clause(
            table_name=target_view,
            source_table_alias="source",
            target_table_alias="databricks",
            join_columns=join_columns,
        )

        return from_clause, join_clause

    def _build_threshold_absolute_case(self, base: exp.Expression, threshold: Thresholds) -> exp.Case:
        eq_if = exp.If(
            this=exp.EQ(this=base, expression=exp.Literal(this='0', is_string=False)),
            true=exp.Identifier(this="Match", quoted=True),
        )
        between_if = exp.If(
            this=exp.Between(
                this=base,
                low=exp.Literal(this=threshold.lower_bound.replace("%", ""), is_string=False),
                high=exp.Literal(this=threshold.upper_bound.replace("%", ""), is_string=False),
            ),
            true=exp.Identifier(this="Warning", quoted=True),
        )
        return exp.Case(ifs=[eq_if, between_if], default=exp.Identifier(this="Failed", quoted=True))

    def _build_threshold_percentage_case(self, base: exp.Expression, threshold: Thresholds) -> exp.Case:
        eq_if = exp.If(
            this=exp.EQ(this=base, expression=exp.Literal(this='0', is_string=False)),
            true=exp.Identifier(this="Match", quoted=True),
        )

        denominator = exp.If(
            this=exp.Or(
                this=exp.EQ(
                    this=exp.Column(this=threshold.column_name, table="databricks"),
                    expression=exp.Literal(this='0', is_string=False),
                ),
                expression=exp.Is(
                    this=exp.Column(
                        this=exp.Identifier(this=threshold.column_name, quoted=False),
                        table=exp.Identifier(this='databricks'),
                    ),
                    expression=exp.Null(),
                ),
            ),
            true=exp.Literal(this="1", is_string=False),
            false=exp.Column(this=threshold.column_name, table="databricks"),
        )

        division = exp.Div(this=base, expression=denominator, typed=False, safe=False)
        percentage = exp.Mul(this=exp.Paren(this=division), expression=exp.Literal(this="100", is_string=False))

        between_if = exp.If(
            this=exp.Between(
                this=percentage,
                low=exp.Literal(this=threshold.lower_bound.replace("%", ""), is_string=False),
                high=exp.Literal(this=threshold.upper_bound.replace("%", ""), is_string=False),
            ),
            true=exp.Identifier(this="Warning", quoted=True),
        )
        return exp.Case(ifs=[eq_if, between_if], default=exp.Identifier(this="Failed", quoted=True))
