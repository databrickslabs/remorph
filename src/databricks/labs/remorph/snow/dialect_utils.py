import logging
from dataclasses import dataclass

from sqlglot import ErrorLevel, exp, parse
from sqlglot.errors import ParseError, TokenError, UnsupportedError
from sqlglot.expressions import Expression, Select

from databricks.labs.remorph.helpers.morph_status import ValidationError
from databricks.labs.remorph.snow.snowflake import Snow

logger = logging.getLogger(__name__)


@dataclass
class _AliasInfo:
    name: str
    expression: exp.Expression
    is_same_name_as_column: bool


def check_for_unsupported_lca(
    dialect: str,
    sql: str,
    filename: str,
) -> ValidationError | None:
    """
    Check for presence of unsupported lateral column aliases in window expressions and where clauses
    :return: An error if found
    """
    if dialect.upper() == "SNOWFLAKE":
        dialect = Snow

    try:
        parsed_expr = parse(sql, read=dialect, error_level=ErrorLevel.RAISE)
    except (ParseError, TokenError, UnsupportedError) as e:
        logger.warning(f"Error while preprocessing {filename}: {e}")
        return None

    aliases_in_where = set()
    aliases_in_window = set()

    for expr in parsed_expr:
        if expr:
            for select in expr.find_all(exp.Select, bfs=False):
                alias_info = _find_aliases_in_select(select)
                aliases_in_where.update(_find_invalid_lca_in_where(select, alias_info))
                aliases_in_window.update(_find_invalid_lca_in_window(select, alias_info))

    if not (aliases_in_where or aliases_in_window):
        return None

    err_messages = [f"Unsupported operation found in file {filename}. Needs manual review of transpiled query."]
    if aliases_in_where:
        err_messages.append(f"Lateral column aliases `{', '.join(aliases_in_where)}` found in where clause.")

    if aliases_in_window:
        err_messages.append(f"Lateral column aliases `{', '.join(aliases_in_window)}` found in window expressions.")

    return ValidationError(filename, " ".join(err_messages))


def fix_unsupported_lca(expr: exp.Expression) -> exp.Expression:
    for select in expr.find_all(exp.Select, bfs=False):
        alias_info = _find_aliases_in_select(select)
        where_ast: Expression = select.args.get("where")
        if where_ast:
            where_ast.transform(
                _replace_alias_with_original_expression,
                alias_info,
                copy=False,
            )
        for window in _find_windows_in_select(select):
            window.transform(
                _replace_alias_with_original_expression,
                alias_info,
                copy=False,
            )
    return expr


def _find_windows_in_select(select: Select) -> list[exp.Window]:
    window_expressions = []
    for expr in select.expressions:
        window_expr = expr.find(exp.Window)
        if window_expr:
            window_expressions.append(window_expr)
    return window_expressions


def _find_aliases_in_select(select_expr: Select) -> dict[str, _AliasInfo]:
    aliases = {}
    for expr in select_expr.expressions:
        if isinstance(expr, exp.Alias):
            alias_name = expr.output_name
            is_same_name_as_column = False
            for column in expr.find_all(exp.Column):
                if column.name == alias_name:
                    is_same_name_as_column = True
                    break
            aliases[alias_name] = _AliasInfo(alias_name, expr.unalias(), is_same_name_as_column)
    return aliases


def _find_invalid_lca_in_where(
    select_expr: Select,
    aliases: dict[str, _AliasInfo],
) -> set[str]:
    aliases_in_where = set()
    where_ast: Expression = select_expr.args.get("where")
    if where_ast:
        for column in where_ast.find_all(exp.Column):
            if column.name in aliases and not aliases[column.name].is_same_name_as_column:
                aliases_in_where.add(column.name)

    return aliases_in_where


def _find_invalid_lca_in_window(
    select_expr: Select,
    aliases: dict[str, _AliasInfo],
) -> set[str]:
    aliases_in_window = set()
    windows = _find_windows_in_select(select_expr)
    for window in windows:
        for column in window.find_all(exp.Column):
            if column.name in aliases and not aliases[column.name].is_same_name_as_column:
                aliases_in_window.add(column.name)

    return aliases_in_window


def _replace_alias_with_original_expression(
    node: Expression,
    alias_info: dict[str, _AliasInfo],
) -> Expression:
    if isinstance(node, exp.Column) and node.name in alias_info and not alias_info[node.name].is_same_name_as_column:
        return alias_info[node.name].expression

    return node
