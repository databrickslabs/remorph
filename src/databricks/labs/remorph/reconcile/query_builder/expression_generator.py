from sqlglot import expressions as exp

from databricks.labs.remorph.reconcile.recon_config import Thresholds


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


def anonymous(node, func: str):
    if isinstance(node, exp.Column):
        column_name = node.name
        table_name = node.table
        return exp.Anonymous(this=func, expressions=[exp.Column(this=column_name, table=table_name)])
    return node


def build_column(this, table_name="", quoted=False) -> exp.Column:
    return exp.Column(this=exp.Identifier(this=this, quoted=quoted), table=table_name)


def build_alias(this: exp.ExpOrStr, alias="", table_name="", quoted=False) -> exp.Alias:
    if isinstance(this, str):
        return exp.Alias(this=build_column(this, table_name), alias=exp.Identifier(this=alias, quoted=quoted))
    return exp.Alias(this=this, alias=exp.Identifier(this=alias, quoted=quoted))


def build_from_clause(table_name: str, table_alias: str) -> exp.From:
    return exp.From(this=exp.Table(this=exp.Identifier(this=table_name), alias=table_alias))


def build_join_clause(table_name: str, table_alias: str, join_columns: list, kind: str = "inner") -> exp.Join:
    join_conditions = []
    for column in join_columns:
        join_condition = exp.NullSafeEQ(
            this=exp.Column(this=column, table="source"), expression=exp.Column(this=column, table=table_alias)
        )
        join_conditions.append(join_condition)

    # Combine all join conditions with AND
    on_condition = join_conditions[0]
    for condition in join_conditions[1:]:
        on_condition = exp.And(this=on_condition, expression=condition)

    return exp.Join(this=exp.Table(this=exp.Identifier(this=table_name), alias=table_alias), kind=kind, on=on_condition)


def build_sub(left_column_name, left_table_name="", right_column_name="", right_table_name="") -> exp.Sub:
    return exp.Sub(
        this=build_column(left_column_name, left_table_name),
        expression=build_column(right_column_name, right_table_name),
    )


def build_threshold_absolute_case(base: exp.Expression, threshold: Thresholds) -> exp.Case:
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


def build_threshold_percentile_case(base: exp.Expression, threshold: Thresholds) -> exp.Case:
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


def build_where_clause(where_clause=list[exp.Expression]) -> exp.Or:
    # Start with a default
    combined_expression = exp.Or(this='1 = 1', expression='1 = 1')

    # Loop through the expressions and combine them with OR
    for expression in where_clause:
        combined_expression = exp.Or(this=combined_expression, expression=expression)

    return combined_expression
