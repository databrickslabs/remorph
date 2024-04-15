from sqlglot import expressions as exp

from databricks.labs.remorph.reconcile.recon_config import Thresholds


class ExpressionGenerator:

    def __init__(self):
        pass

    @staticmethod
    def coalesce(node, default="0", is_string=False):
        if isinstance(node, exp.Column):
            column_name = node.name
            table_name = node.table
            return exp.Coalesce(
                this=exp.Column(this=column_name, table=table_name),
                expressions=[exp.Literal(this=default, is_string=is_string)],
            )
        if isinstance(node, exp.Anonymous):
            this = node.this
            expressions = node.expressions
            return exp.Coalesce(
                this=exp.Anonymous(this=this, expressions=expressions),
                expressions=exp.Literal(this=default, is_string=is_string),
            )
        return node

    @staticmethod
    def paran(node):
        return exp.Paren(this=node)

    @staticmethod
    def anonymous(node, func: str):
        if isinstance(node, exp.Column):
            column_name = node.name
            table_name = node.table
            return exp.Anonymous(this=func, expressions=[exp.Column(this=column_name, table=table_name)])
        return node

    @staticmethod
    def build_column(this, table_name="", quoted=False):
        return exp.Column(this=exp.Identifier(this=this, quoted=quoted), table=table_name)

    def build_alias(self, this: exp.ExpOrStr, alias="", table_name="", quoted=False):
        if isinstance(this, str):
            return exp.Alias(this=self.build_column(this, table_name), alias=exp.Identifier(this=alias, quoted=quoted))
        return exp.Alias(this=this, alias=exp.Identifier(this=alias, quoted=quoted))

    def build_sub(self, left_column_name, left_table_name="", right_column_name="", right_table_name=""):
        return exp.Sub(
            this=self.build_column(left_column_name, left_table_name),
            expression=self.build_column(right_column_name, right_table_name),
        )

    @staticmethod
    def build_absolute_case(base: exp.Expression, threshold: Thresholds):
        eq_if = exp.If(
            this=exp.EQ(this=base, expression=exp.Literal(this='0', is_string=False)),
            true=exp.Identifier(this="Match", quoted=True),
        )
        between_if = exp.If(
            this=exp.Between(
                this=base,
                low=exp.Literal(this=threshold.lower_bound, is_string=False),
                high=exp.Literal(this=threshold.upper_bound, is_string=False),
            ),
            true=exp.Identifier(this="Warning", quoted=True),
        )
        return exp.Case(ifs=[eq_if, between_if], default=exp.Identifier(this="Failed", quoted=True))

    @staticmethod
    def build_percentile_case(base: exp.Expression, threshold: Thresholds):
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

    @staticmethod
    def build_where_clause(where_clause=list[exp.Expression]):
        # Start with the first expression
        combined_expression = where_clause[0]

        # Loop through the rest of the expressions and combine them with OR
        for expression in where_clause[1:]:
            combined_expression = exp.Or(this=combined_expression, expression=expression)

        return combined_expression

    @staticmethod
    def build_from_clause(table_name: str):
        return exp.From(this=exp.Table(this=exp.Identifier(this=table_name), alias="source"))

    @staticmethod
    def build_join_clause(table_name: str, join_columns: list):
        join_conditions = []
        for column in join_columns:
            join_condition = exp.NullSafeEQ(
                this=exp.Column(this=column, table="source"), expression=exp.Column(this=column, table="databricks")
            )
            join_conditions.append(join_condition)

        # Combine all join conditions with AND
        on_condition = join_conditions[0]
        for condition in join_conditions[1:]:
            on_condition = exp.And(this=on_condition, expression=condition)

        return exp.Join(
            this=exp.Table(this=exp.Identifier(this=table_name), alias="databricks"), kind="inner", on=on_condition
        )
