from collections.abc import Callable
from functools import partial

from sqlglot import expressions as exp
from sqlglot.expressions import (
    Alias,
    Anonymous,
    Coalesce,
    Column,
    DataType,
    Expression,
    From,
    Join,
    JSONFormat,
    Literal,
    Trim,
)


def coalesce(expr: Expression, default="0", is_string=False) -> Coalesce | Expression:
    level = 0 if isinstance(expr, exp.Column) else 1
    new_expr = expr.copy()
    for node in new_expr.dfs():
        if isinstance(node, exp.Column):
            column_name = node.name
            table_name = node.table
            func = exp.Coalesce(
                this=exp.Column(this=column_name, table=table_name),
                expressions=[exp.Literal(this=default, is_string=is_string)],
            )
            if level == 0:
                return func
            node.replace(func)
    return new_expr


def trim(expr: Expression) -> Trim | Expression:
    level = 0 if isinstance(expr, exp.Column) else 1
    new_expr = expr.copy()
    for node in new_expr.dfs():
        if isinstance(node, exp.Column):
            column_name = node.name
            table_name = node.table
            func = exp.Trim(this=exp.Column(this=column_name, table=table_name))
            if level == 0:
                return func
            node.replace(func)
    return new_expr


def json_format(expr: Expression, options: dict[str, str] | None = None) -> JSONFormat | Expression:
    level = 0 if isinstance(expr, exp.Column) else 1
    new_expr = expr.copy()
    for node in new_expr.dfs():
        if isinstance(node, exp.Column):
            column_name = node.name
            table_name = node.table
            func = exp.JSONFormat(this=exp.Column(this=column_name, table=table_name), options=options)
            if level == 0:
                return func
            node.replace(func)
    return new_expr


def anonymous(node, func: str) -> Anonymous | Expression:
    if isinstance(node, exp.Column):
        column_name = node.name
        table_name = node.table
        return exp.Anonymous(this=func, expressions=[exp.Column(this=column_name, table=table_name)])
    return node


def build_column(this, table_name="", quoted=False) -> Column:
    return exp.Column(this=exp.Identifier(this=this, quoted=quoted), table=table_name)


def build_literal(this, is_string=True) -> Literal:
    return exp.Literal(this=this, is_string=is_string)


def build_literal_alias(this: exp.ExpOrStr, alias="", quoted=False, is_string=True) -> Alias:
    return exp.Alias(this=build_literal(this, is_string=is_string), alias=exp.Identifier(this=alias, quoted=quoted))


def build_alias(this: exp.ExpOrStr, alias="", table_name="", quoted=False) -> Alias:
    if isinstance(this, str):
        return exp.Alias(this=build_column(this, table_name), alias=exp.Identifier(this=alias, quoted=quoted))
    return exp.Alias(this=this, alias=exp.Identifier(this=alias, quoted=quoted))


def build_from_clause(table_name: str, table_alias: str) -> From:
    return exp.From(this=exp.Table(this=exp.Identifier(this=table_name), alias=table_alias))


def build_join_clause(table_name: str, table_alias: str, join_columns: list, kind: str = "inner") -> Join:
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


def preprocess(expr: Expression, funcs: list[Callable[[exp.Expression], exp.Expression]]) -> Expression:
    for func in funcs:
        expr = func(expr)
    assert isinstance(expr, exp.Expression), (
        f"Func returned an instance of type [{type(expr)}], " "should have been Expression."
    )
    return expr


DataType_transform_mapping = {
    DataType.Type.VARCHAR.value: [partial(coalesce, default='', is_string=True), trim],
    DataType.Type.MAP.value: [json_format],
    "NUMBER": [partial(coalesce, default='', is_string=True), trim],
}
