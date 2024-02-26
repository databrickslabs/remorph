import logging

from sqlglot import ErrorLevel, exp, parse
from sqlglot.errors import ParseError, TokenError, UnsupportedError
from sqlglot.expressions import Expression, Select

from databricks.labs.remorph.helpers.morph_status import ValidationError
from databricks.labs.remorph.snow.snowflake import Snow

logger = logging.getLogger(__name__)


def find_windows_in_select(select: Select) -> list[exp.Window]:
    window_expressions = []
    for expr in select.expressions:
        window_expr = expr.find(exp.Window)
        if window_expr:
            window_expressions.append(window_expr)
    return window_expressions


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
                alias_names = {alias.output_name for alias in select.expressions if isinstance(alias, exp.Alias)}
                aliases_in_where.update(_find_invalid_lca_in_where(select, alias_names))
                aliases_in_window.update(_find_invalid_lca_in_window(select, alias_names))

    if not (aliases_in_where or aliases_in_window):
        return None

    err_messages = [f"Unsupported operation found in file {filename}. Needs manual review of transpiled query."]
    if aliases_in_where:
        err_messages.append(f"Lateral column aliases `{', '.join(aliases_in_where)}` found in where clause.")

    if aliases_in_window:
        err_messages.append(f"Lateral column aliases `{', '.join(aliases_in_window)}` found in window expressions.")

    return ValidationError(filename, " ".join(err_messages))


def _find_invalid_lca_in_where(
    select_expr: Select,
    aliases: set[str],
) -> set[str]:
    aliases_in_where = set()
    where_ast: Expression = select_expr.args.get("where")
    if where_ast:
        for column in where_ast.find_all(exp.Column):
            if column.name in aliases:
                aliases_in_where.add(column.name)

    return aliases_in_where


def _find_invalid_lca_in_window(
    select_expr: Select,
    aliases: set[str],
) -> set[str]:
    aliases_in_window = set()
    windows = find_windows_in_select(select_expr)
    for window in windows:
        for column in window.find_all(exp.Column):
            if column.name in aliases:
                aliases_in_window.add(column.name)

    return aliases_in_window
