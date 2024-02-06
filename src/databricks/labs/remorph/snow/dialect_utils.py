from sqlglot import ErrorLevel, exp, parse
from sqlglot.expressions import Expression

from databricks.labs.remorph.helpers.morph_status import ParseError, ValidationError
from databricks.labs.remorph.snow.snowflake import Snow


def check_for_unsupported_lca(
    dialect: str,
    sql: str,
    filename: str,
) -> ValidationError | ParseError | None:
    """
    Check for presence of unsupported lateral column aliases in window expressions and where clauses
    :return: A list of errors if found
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
            for select in expr.find_all(exp.Select):
                erroneous_aliases.update(_find_invalid_lca_in_select(select))
    if erroneous_aliases:
        err_message = (
            f"Unsupported operation found in file {filename}. "
            f"Lateral column aliases `{', '.join(erroneous_aliases)}` found in "
            f"window expression or where clause. Needs manual review."
        )
        return ValidationError(filename, err_message)
    else:
        return None


def _find_invalid_lca_in_select(
    select: Expression,
) -> list[str]:
    erroneous_alias_list = []
    alias_names = {alias.output_name for alias in select.find_all(exp.Alias)}
    for child in select.find_all(exp.Window, exp.Where):
        for column in child.find_all(exp.Column):
            if column.name in alias_names:
                erroneous_alias_list.append(column.name)
    return erroneous_alias_list
