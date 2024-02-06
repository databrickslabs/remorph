from sqlglot import ErrorLevel, exp, parse
from sqlglot.expressions import Expression, Select

from databricks.labs.remorph.helpers.morph_status import ParseError, ValidationError
from databricks.labs.remorph.snow.snowflake import Snow


def find_windows_in_select(select: Select):
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
) -> ValidationError | ParseError | None:
    """
    Check for presence of unsupported lateral column aliases in window expressions and where clauses
    :return: An error if found
    """
    if dialect.upper() == "SNOWFLAKE":
        dialect = Snow

    try:
        parsed_expr = parse(sql, read=dialect, error_level=ErrorLevel.RAISE)
    except Exception as e:
        return ParseError(filename, f"Error while preprocessing {filename}: {e}")

    erroneous_aliases = set()
    for expr in parsed_expr:
        if expr:
            for select in expr.find_all(exp.Select, bfs=False):
                erroneous_aliases.update(_find_invalid_lca_in_select(select))
    if erroneous_aliases:
        err_message = (
            f"Unsupported operation found in file {filename}. "
            f"Lateral column aliases `{', '.join(erroneous_aliases)}` found in "
            f"window expression or where clause. Needs manual review of transpiled query."
        )
        return ValidationError(filename, err_message)
    else:
        return None


def _find_invalid_lca_in_select(
    select_expr: Select,
) -> set[str]:
    erroneous_aliases = set()
    aliases = {alias.output_name for alias in select_expr.expressions if isinstance(alias, exp.Alias)}
    where_ast: Expression = select_expr.args.get("where")
    if where_ast:
        for column in where_ast.find_all(exp.Column):
            if column.name in aliases:
                erroneous_aliases.add(column.name)

    windows = find_windows_in_select(select_expr)
    for window in windows:
        for column in window.find_all(exp.Column):
            if column.name in aliases:
                erroneous_aliases.add(column.name)

    return erroneous_aliases
