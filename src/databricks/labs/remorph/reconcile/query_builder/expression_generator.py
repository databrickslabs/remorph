from sqlglot import expressions as exp


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


def build_column(this, table_name="", quoted=False):
    return exp.Column(this=exp.Identifier(this=this, quoted=quoted), table=table_name)


def build_alias(this: exp.ExpOrStr, alias="", table_name="", quoted=False):
    if isinstance(this, str):
        return exp.Alias(this=build_column(this, table_name), alias=exp.Identifier(this=alias, quoted=quoted))
    return exp.Alias(this=this, alias=exp.Identifier(this=alias, quoted=quoted))


def build_from_clause(table_name: str, table_alias: str):
    return exp.From(this=exp.Table(this=exp.Identifier(this=table_name), alias=table_alias))


def build_join_clause(table_name: str, table_alias: str, join_columns: list, kind: str = "inner"):
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
