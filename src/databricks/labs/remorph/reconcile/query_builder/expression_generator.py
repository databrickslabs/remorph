from collections.abc import Callable
from functools import partial

from sqlglot import expressions as exp


def _apply_func_expr(expr: exp.Expression, expr_func: Callable, **kwargs) -> exp.Expression:
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


def coalesce(expr: exp.Expression, default="0", is_string=False) -> exp.Coalesce | exp.Expression:
    expressions = [exp.Literal(this=default, is_string=is_string)]
    return _apply_func_expr(expr, exp.Coalesce, expressions=expressions)


def trim(expr: exp.Expression) -> exp.Trim | exp.Expression:
    return _apply_func_expr(expr, exp.Trim)


def json_format(expr: exp.Expression, options: dict[str, str] | None = None) -> exp.JSONFormat | exp.Expression:
    return _apply_func_expr(expr, exp.JSONFormat, options=options)


def sort_array(expr: exp.Expression, asc=True):
    return _apply_func_expr(expr, exp.SortArray, asc=exp.Boolean(this=asc))


def to_char(expr: exp.Expression, to_format=None, nls_param=None):
    if to_format:
        return _apply_func_expr(
            expr, exp.ToChar, format=exp.Literal(this=to_format, is_string=True), nls_param=nls_param
        )
    return _apply_func_expr(expr, exp.ToChar)


def array_to_string(
    expr: exp.Expression,
    delimiter: str = ",",
    is_string=True,
    null_replacement: str | None = None,
    is_null_replace=True,
):
    if null_replacement:
        return _apply_func_expr(
            expr,
            exp.ArrayToString,
            expression=[exp.Literal(this=delimiter, is_string=is_string)],
            null=exp.Literal(this=null_replacement, is_string=is_null_replace),
        )
    return _apply_func_expr(expr, exp.ArrayToString, expression=[exp.Literal(this=delimiter, is_string=is_string)])


def array_sort(expr: exp.Expression, asc=True):
    return _apply_func_expr(expr, exp.ArraySort, expression=exp.Boolean(this=asc))


def anonymous(expr: exp.Expression, func: str) -> exp.Anonymous | exp.Expression:
    """

    This function used in cases where the sql functions are not available in sqlGlot expressions
    Example:
        >>> from sqlglot import parse_one
        >>> print(repr(parse_one('select unix_timestamp(col1)')))

    the above code gives you a Select Expression of Anonymous function.

    To achieve the same,we can use the function as below:
    eg:
        >>> expr = parse_one("select col1 from dual")
        >>> transformed_expr=anonymous(expr,"unix_timestamp")
        >>> print(transformed_expr)
        'SELECT UNIX_TIMESTAMP(col1) FROM DUAL'

    """
    new_expr = expr.copy()
    for node in new_expr.dfs():
        if isinstance(node, exp.Column):
            return exp.Column(this=func.format(node.name))
    return new_expr


def build_column(this: exp.ExpOrStr, table_name="", quoted=False, alias=None) -> exp.Alias | exp.Column:
    if alias:
        if isinstance(this, str):
            return exp.Alias(
                this=exp.Column(this=this, table_name=table_name), alias=exp.Identifier(this=alias, quoted=quoted)
            )
        return exp.Alias(this=this, alias=exp.Identifier(this=alias, quoted=quoted))
    return exp.Column(this=exp.Identifier(this=this, quoted=quoted), table=table_name)


def build_literal(this: exp.ExpOrStr, alias=None, quoted=False, is_string=True) -> exp.Alias | exp.Literal:
    if alias:
        return exp.Alias(
            this=exp.Literal(this=this, is_string=is_string), alias=exp.Identifier(this=alias, quoted=quoted)
        )
    return exp.Literal(this=this, is_string=is_string)


def transform_expression(
    expr: exp.Expression, funcs: list[Callable[[exp.Expression], exp.Expression]]
) -> exp.Expression:
    for func in funcs:
        expr = func(expr)
    assert isinstance(expr, exp.Expression), (
        f"Func returned an instance of type [{type(expr)}], " "should have been Expression."
    )
    return expr


DataType_transform_mapping = {
    "default": [partial(coalesce, default='', is_string=True), trim],
    "snowflake": {exp.DataType.Type.ARRAY.value: [array_to_string, array_sort]},
    "oracle": {
        exp.DataType.Type.NCHAR.value: [partial(anonymous, func="nvl(trim(to_char({})),'_null_recon_')")],
        exp.DataType.Type.NVARCHAR.value: [partial(anonymous, func="nvl(trim(to_char({})),'_null_recon_')")],
    },
    "databricks": {
        exp.DataType.Type.ARRAY.value: [partial(anonymous, func="concat_ws(',', sort_array({}))")],
    },
}
