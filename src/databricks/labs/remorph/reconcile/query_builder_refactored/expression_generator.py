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


def _apply_func_expr(expr, expr_func, **kwargs):
    level = 0 if isinstance(expr, exp.Column) else 1
    new_expr = expr.copy()
    for node in new_expr.dfs():
        if isinstance(node, exp.Column):
            column_name = node.name
            table_name = node.table
            func = expr_func(this=exp.Column(this=column_name, table=table_name), **kwargs)
            if level == 0:
                return func
            node.replace(func)
    return new_expr


def coalesce(expr: Expression, default="0", is_string=False) -> Coalesce | Expression:
    expressions = [exp.Literal(this=default, is_string=is_string)]
    return _apply_func_expr(expr, exp.Coalesce, expressions=expressions)


def trim(expr: Expression) -> Trim | Expression:
    return _apply_func_expr(expr, exp.Trim)


def json_format(expr: Expression, options: dict[str, str] | None = None) -> JSONFormat | Expression:
    return _apply_func_expr(expr, exp.JSONFormat, options=options)


def sort_array(expr: Expression, asc=False):
    return _apply_func_expr(expr, exp.SortArray, asc=asc)


def concat_ws(expr: Expression):
    return _apply_func_expr(expr, exp.ArrayConcat)


def to_char(expr: Expression, to_format=None, nls_param=None):
    return _apply_func_expr(expr, exp.ToChar, format=to_format, nls_param=nls_param)


def array_to_string(expr: Expression, delimiter: str = ",", null_replacement: str | None = None):
    return _apply_func_expr(expr, exp.ArrayToString, expression=[exp.Literal(this=delimiter)], null=null_replacement)


def array_sort(expr: Expression):
    return _apply_func_expr(expr, exp.ArraySort)


def anonymous(expr: Expression, func: str) -> Anonymous | Expression:
    new_expr = expr.copy()
    for node in new_expr.dfs():
        if isinstance(node, exp.Column):
            return exp.Column(this=func.format(node.name))
    return new_expr


def build_column(this, table_name="", quoted=False, alias=None) -> Alias | Column:
    if alias:
        if isinstance(this, str):
            return exp.Alias(
                this=exp.Column(this=this, table_name=table_name), alias=exp.Identifier(this=alias, quoted=quoted)
            )
        return exp.Alias(this=this, alias=exp.Identifier(this=alias, quoted=quoted))
    return exp.Column(this=exp.Identifier(this=this, quoted=quoted), table=table_name)


def build_literal(this: exp.ExpOrStr, alias=None, quoted=False, is_string=True) -> Alias | Literal:
    if alias:
        return exp.Alias(
            this=exp.Literal(this=this, is_string=is_string), alias=exp.Identifier(this=alias, quoted=quoted)
        )
    return exp.Literal(this=this, is_string=is_string)


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


def transform_expression(expr: Expression, funcs: list[Callable[[exp.Expression], exp.Expression]]) -> Expression:
    for func in funcs:
        expr = func(expr)
    assert isinstance(expr, exp.Expression), (
        f"Func returned an instance of type [{type(expr)}], " "should have been Expression."
    )
    return expr


DataType_transform_mapping = {
    "default": [partial(coalesce, default='', is_string=True), trim],
    "snowflake": {
        DataType.Type.ARRAY.value: [array_to_string, array_sort]
    },
    "oracle": {
        DataType.Type.NCHAR.value: [partial(anonymous, func="nvl(trim(to_char({})),'_null_recon_')")],
        DataType.Type.NVARCHAR.value: [partial(anonymous, func="nvl(trim(to_char({})),'_null_recon_')")],
    },
    "databricks": {
        DataType.Type.ARRAY.value: [concat_ws, sort_array]
    }
}
