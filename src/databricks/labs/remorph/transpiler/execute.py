import os
import sys

from sqlglot import transpile

from databricks.labs.remorph.helpers.execution_time import timeit
from databricks.labs.remorph.helpers.validate import Validate
from databricks.labs.remorph.snow.databricks import Databricks
from databricks.labs.remorph.snow.snowflake import Snow


def validate_query(sql: str, connection_mode: str, catalog_nm, schema_nm):
    """
    Validates the SQL query based on the connection mode, catalog name, and schema name.

    :param sql: The SQL query to be validated.
    :param connection_mode: The mode of the connection.
    :param catalog_nm: The name of the catalog.
    :param schema_nm: The name of the schema.
    :return: Boolean indicating whether the query is valid or not.
    """
    validate = Validate(connection_mode=connection_mode)
    return validate.query(sql, catalog_nm, schema_nm)


def convert(dialect, sql, file_nm, error_list):
    """
    Converts the SQL query from one dialect to another.

    :param dialect: The dialect to convert the SQL query to.
    :param sql: The SQL query to be converted.
    :param file_nm: The name of the file containing the SQL query.
    :param error_list: The list to store any errors that occur during conversion.
    :return: The converted SQL query.
    """
    if dialect.upper() == "SNOWFLAKE":
        dialect = Snow
    else:
        dialect = dialect.lower()

    try:
        transpiled_sql = transpile(sql, read=dialect, write=Databricks, pretty=True, error_level=None)
    except Exception as e:
        transpiled_sql = ""
        error_list.append((file_nm, e))

    return transpiled_sql


@timeit
def morph(
    source,
    input_sql,
    output_folder,
    skip_validation="false",
    validation_mode="LOCAL_REMOTE",
    catalog_nm="transpiler_test",
    schema_nm="convertor_test",
):
    """
    Transpiles the SQL queries from one dialect to another.

    :param source: The source dialect of the SQL queries.
    :param input_sql: The directory containing the SQL queries.
    :param output_folder: The directory to store the transpiled SQL queries.
    :param skip_validation: Whether to skip validation of the SQL queries.
    :param validation_mode: The mode of validation.
    :param catalog_nm: The name of the catalog.
    :param schema_nm: The name of the schema.
    """
    file_list = []
    parse_error_list = []
    validate_error_list = []
    status = []

    print("**********************************", file=sys.stderr)  # noqa: T201
    counter = 0
    for root, _, files in os.walk(input_sql):
        base_root = root.replace(input_sql, "")
        folder = input_sql.rstrip("/") + "/" + base_root
        msg = f"Processing for sqls under this folder: {folder}"
        print(msg, file=sys.stderr)  # noqa: T201
        file_list.extend(files)
        for file in files:
            if output_folder in (None, "None"):
                output_folder_base = root + "/transpiled"
            else:
                output_folder_base = output_folder.rstrip("/") + "/" + base_root

            output_file_name = output_folder_base + "/" + file

            if not os.path.exists(output_folder_base):
                os.makedirs(output_folder_base, exist_ok=True)

            f = open(root + "/" + file)
            sql = f.read()

            transpiled_sql = convert(source, sql, file, parse_error_list)

            w = open(output_file_name, "w")
            for output in transpiled_sql:
                # [TODO] : Naive way to skip any alter session or begin or commit This is bad design.
                if (
                    output.lower() not in ("", None)
                    and "alter session set query_tag" not in output.lower()
                    and "begin" not in output.lower()
                    and "commit" not in output.lower()
                    and "stream" not in output.lower()
                    and "task" not in output.lower()
                    and "procedure" not in output.lower()
                ):
                    counter = counter + 1
                    if skip_validation:
                        w.write(output)
                        w.write("\n;\n")
                    else:
                        (flag, exception) = validate_query(output, validation_mode, catalog_nm, schema_nm)
                        if flag:
                            w.write(output)
                            w.write("\n;\n")
                        else:
                            w.write("-------------- Exception Start-------------------\n")
                            w.write(f"/* \n {exception} \n */ \n")
                            if "[UNRESOLVED_ROUTINE]" in exception:
                                w.write(f"/* \n {output} \n */ \n")
                            w.write("\n ---------------Exception End --------------------\n")
                            validate_error_list.append((file, exception))
                else:
                    pass

            w.close()

    error_list_count = len(parse_error_list) + len(validate_error_list)

    if skip_validation:
        pass
    else:
        print("No of Sql Failed while Validating: ", len(validate_error_list), file=sys.stderr)  # noqa: T201

    error_list = parse_error_list + validate_error_list
    if error_list_count > 0:
        error_list_file = os.getcwd() + f"/err_{os.getpid()}.lst"
        e = open(error_list_file, "a")
        for err in error_list:
            e.write(str(err) + "\n")
        e.close()
    else:
        error_list_file = None

    status.append(
        {
            "total_files_processed": len(file_list),
            "total_queries_processed": counter,
            "no_of_sql_failed_while_parsing": len(parse_error_list),
            "no_of_sql_failed_while_validating": len(validate_error_list),
            "error_list_file": error_list_file,
        }
    )
    return status
