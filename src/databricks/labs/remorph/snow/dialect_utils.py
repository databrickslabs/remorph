from sqlglot import ErrorLevel, exp, parse

from databricks.labs.remorph.snow.snowflake import Snow


def check_for_unsupported_lca(dialect, sql, filename, error_list):
    # Check for presence of unsupported lateral column aliases in window expressions and where clauses
    if dialect.upper() == "SNOWFLAKE":
        dialect = Snow
    try:
        for expr in parse(sql, read=dialect, error_level=ErrorLevel.IGNORE):
            if not expr:
                continue
            for select in expr.find_all(exp.Select):
                alias_names = {alias.output_name for alias in select.find_all(exp.Alias)}
                for window in select.find_all(exp.Window):
                    for column in window.find_all(exp.Column):
                        if column.name in alias_names:
                            error_list.append(
                                (
                                    filename,
                                    f"Unsupported operation found in file {filename}. "
                                    f"Lateral column alias `{column.name}` found in window expression. "
                                    f"Needs manual review.",
                                )
                            )
                for where in select.find_all(exp.Where):
                    for column in where.find_all(exp.Column):
                        if column.name in alias_names:
                            error_list.append(
                                (
                                    filename,
                                    f"Unsupported operation found in file {filename}. "
                                    f"Lateral column alias `{column.name}` found in where clause. Needs manual review.",
                                )
                            )
    except Exception as e:
        error_list.append((filename, f"Error while preprocessing {filename}: {e}"))
