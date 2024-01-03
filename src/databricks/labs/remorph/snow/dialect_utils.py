from sqlglot import ErrorLevel, exp, parse
from sqlglot.expressions import Expression

from databricks.labs.remorph.snow.snowflake import Snow


def check_for_unsupported_lca(
    dialect: str,
    sql: str,
    filename: str,
    error_list: list[tuple[str, str]],
):
    """Check for presence of unsupported lateral column aliases in window expressions and where clauses"""
    if dialect.upper() == "SNOWFLAKE":
        dialect = Snow
    try:
        for expr in parse(sql, read=dialect, error_level=ErrorLevel.IGNORE):
            if expr:
                for select in expr.find_all(exp.Select):
                    _check_lca_usage_in_select(select, filename, error_list)
    except Exception as e:
        error_list.append((filename, f"Error while preprocessing {filename}: {e}"))


def _check_lca_usage_in_select(
    select: Expression,
    filename: str,
    error_list: list[tuple[str, str]],
):
    alias_names = {alias.output_name for alias in select.find_all(exp.Alias)}
    for child in select.find_all(exp.Window, exp.Where):
        for column in child.find_all(exp.Column):
            if column.name in alias_names:
                err_message = (
                    f"Unsupported operation found in file {filename}. "
                    f"Lateral column alias `{column.name}` found in window expression or where clause. "
                    "Needs manual review."
                )
                error_list.append((filename, err_message))
