from sqlglot import ErrorLevel, exp, parse
from sqlglot.expressions import Expression

from databricks.labs.remorph.helpers.morph_status import ParseError, ValidationError
from databricks.labs.remorph.snow.snowflake import Snow


def check_for_unsupported_lca(
    dialect: str,
    sql: str,
    filename: str,
) -> list[ValidationError | ParseError]:
    """
    Check for presence of unsupported lateral column aliases in window expressions and where clauses
    :return: A list of errors if found
    """
    error_list = []

    if dialect.upper() == "SNOWFLAKE":
        dialect = Snow
    try:
        for expr in parse(sql, read=dialect, error_level=ErrorLevel.RAISE):
            if expr:
                for select in expr.find_all(exp.Select):
                    error_list.extend(_check_lca_usage_in_select(select, filename))
    except Exception as e:
        error_list.append(ParseError(filename, f"Error while preprocessing {filename}: {e}"))

    return error_list


def _check_lca_usage_in_select(
    select: Expression,
    filename: str,
) -> list[ValidationError]:
    error_list = []
    alias_names = {alias.output_name for alias in select.find_all(exp.Alias)}
    for child in select.find_all(exp.Window, exp.Where):
        for column in child.find_all(exp.Column):
            if column.name in alias_names:
                err_message = (
                    f"Unsupported operation found in file {filename}. "
                    f"Lateral column alias `{column.name}` found in window expression or where clause. "
                    "Needs manual review."
                )
                error_list.append(ValidationError(filename, err_message))

    return error_list
