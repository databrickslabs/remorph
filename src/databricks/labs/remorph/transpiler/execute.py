import os
import sys

from databricks.labs.remorph.config import MorphConfig, MorphStatus
from databricks.labs.remorph.helpers.execution_time import timeit
from databricks.labs.remorph.helpers.utils import is_sql_file, remove_bom
from databricks.labs.remorph.helpers.validate import Validate
from databricks.labs.remorph.snow.sql_transpiler import SQLTranspiler


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


def format_validation_result(config, output):
    validation_mode = config.validation_mode
    catalog_nm = config.catalog_nm
    schema_nm = config.schema_nm
    (flag, exception) = validate_query(output, validation_mode, catalog_nm, schema_nm)
    if flag:
        result = output + "\n;\n"
        exception = None
    else:
        query = ""
        if "[UNRESOLVED_ROUTINE]" in exception:
            query = f"/* \n {output} \n */ \n"
        result = (
            "-------------- Exception Start-------------------\n"
            + f"/* \n {exception} \n */ \n"
            + query
            + "\n ---------------Exception End --------------------\n"
        )

    return result, exception


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def process_file(config: MorphConfig, input_file, output_file):
    source = config.source
    skip_validation = config.skip_validation

    parse_error_list = []
    validate_error_list = []
    no_of_sqls = 0

    with open(input_file) as f:
        sql = remove_bom(f.read())

    transpiler = SQLTranspiler(source, sql, input_file, parse_error_list)
    transpiled_sql = transpiler.transpile()

    with open(output_file, "w") as w:
        for output in transpiled_sql:
            # [TODO] : Naive way to skip any alter session or begin or commit This is bad design.
            output_lower = output.lower() if output else ""
            if (
                output_lower not in ("", None)
                and "alter session set query_tag" not in output_lower
                and "begin" not in output_lower
                and "commit" not in output_lower
                and "stream" not in output_lower
                and "task" not in output_lower
                and "procedure" not in output_lower
            ):
                no_of_sqls = no_of_sqls + 1

                if skip_validation == "true":
                    w.write(output)
                    w.write("\n;\n")
                else:
                    output_string, exception = format_validation_result(config, output)
                    w.write(output_string)
                    if exception is not None:
                        validate_error_list.append((input_file, exception))

            else:
                pass

    return no_of_sqls, parse_error_list, validate_error_list


def process_directory(config: MorphConfig, root, base_root, files):
    output_folder = config.output_folder
    parse_error_list = []
    validate_error_list = []
    counter = 0

    for file in files:
        if is_sql_file(file):
            if output_folder in (None, "None"):
                output_folder_base = root + "/transpiled"
            else:
                output_folder_base = output_folder.rstrip("/") + "/" + base_root

            output_file_name = output_folder_base + "/" + file

            make_dir(output_folder_base)

            input_file = root.rstrip("/") + "/" + file

            no_of_sqls, parse_error, validation_error = process_file(config, input_file, output_file_name)
            counter = counter + no_of_sqls
            parse_error_list.extend(parse_error)
            validate_error_list.extend(validation_error)
        else:
            # Only SQL files are processed with extension .sql or .ddl
            pass

    return counter, parse_error_list, validate_error_list


def process_recursive_dirs(config: MorphConfig):
    input_sql = config.input_sql
    parse_error_list = []
    validate_error_list = []

    file_list = []
    counter = 0
    for root, _, files in os.walk(input_sql):
        base_root = root.replace(input_sql, "")
        folder = input_sql.rstrip("/") + "/" + base_root
        msg = f"Processing for sqls under this folder: {folder}"
        print(msg, file=sys.stderr)  # noqa: T201
        file_list.extend(files)
        no_of_sqls, parse_error, validation_error = process_directory(config, root, base_root, files)
        counter = counter + no_of_sqls
        parse_error_list.extend(parse_error)
        validate_error_list.extend(validation_error)

    error_log = parse_error_list + validate_error_list

    return MorphStatus(file_list, counter, len(parse_error_list), len(validate_error_list), error_log)


@timeit
def morph(config: MorphConfig):
    """
    Transpiles the SQL queries from one dialect to another.

    :param config: The configuration for the morph operation.
    """
    input_sql = config.input_sql
    skip_validation = config.skip_validation
    status = []

    print("**********************************", file=sys.stderr)  # noqa: T201

    if os.path.isfile(input_sql):
        if is_sql_file(input_sql):
            msg = f"Processing for sqls under this file: {input_sql}"
            print(msg, file=sys.stderr)  # noqa: T201
            if config.output_folder in (None, "None"):
                output_folder = os.path.dirname(input_sql) + "/transpiled/"
            else:
                output_folder = config.output_folder.rstrip("/") + "/"
            make_dir(output_folder)
            output_file = output_folder + os.path.basename(input_sql)
            no_of_sqls, parse_error, validation_error = process_file(config, input_sql, output_file)
            error_log = parse_error + validation_error
            result = MorphStatus([input_sql], no_of_sqls, len(parse_error), len(validation_error), error_log)
        else:
            msg = f"{input_sql} is not a SQL file."
            print(msg, file=sys.stderr)  # noqa: T201
    elif os.path.isdir(input_sql):
        result = process_recursive_dirs(config)
    else:
        msg = f"{input_sql} does not exist."
        print(msg, file=sys.stderr)  # noqa: T201
        raise FileNotFoundError(msg)

    parse_error_count = result.parse_error_count
    validate_error_count = result.validate_error_count

    error_list_count = parse_error_count + validate_error_count

    if skip_validation:
        pass
    else:
        print("No of Sql Failed while Validating: ", validate_error_count, file=sys.stderr)  # noqa: T201

    if error_list_count > 0:
        error_log_file = os.getcwd() + f"/err_{os.getpid()}.lst"
        with open(error_log_file, "a") as e:
            e.writelines(f"{err}\n" for err in result.error_log_list)
    else:
        error_log_file = None

    status.append(
        {
            "total_files_processed": len(result.file_list),
            "total_queries_processed": result.no_of_queries,
            "no_of_sql_failed_while_parsing": parse_error_count,
            "no_of_sql_failed_while_validating": validate_error_count,
            "error_log_file": error_log_file,
        }
    )
    print(status, file=sys.stderr)  # noqa: T201
    return status
