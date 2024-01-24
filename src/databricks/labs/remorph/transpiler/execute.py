import os
from pathlib import Path

from databricks.labs.blueprint.entrypoint import get_logger

from databricks.labs.remorph.config import MorphConfig
from databricks.labs.remorph.helpers.execution_time import timeit
from databricks.labs.remorph.helpers.file_utils import (
    dir_walk,
    is_sql_file,
    make_dir,
    remove_bom,
)
from databricks.labs.remorph.helpers.morph_status import MorphStatus, ValidationError
from databricks.labs.remorph.helpers.validate import Validate
from databricks.labs.remorph.snow import dialect_utils
from databricks.labs.remorph.snow.sql_transpiler import SQLTranspiler

logger = get_logger(__file__)


def process_file(config: MorphConfig, input_file: str | Path, output_file: str | Path):
    source = config.source
    skip_validation = config.skip_validation

    parse_error_list = []
    validate_error_list = []
    no_of_sqls = 0

    input_file = Path(input_file)
    output_file = Path(output_file)

    with input_file.open() as f:
        sql = remove_bom(f.read())

    lca_error_list = dialect_utils.check_for_unsupported_lca(source, sql, str(input_file))
    parse_error_list.extend(lca_error_list)
    transpiler = SQLTranspiler(source, sql, str(input_file), parse_error_list)
    transpiled_sql = transpiler.transpile()

    with output_file.open("w") as w:
        for output in transpiled_sql:
            if output:
                no_of_sqls = no_of_sqls + 1
                if skip_validation:
                    w.write(output)
                    w.write("\n;\n")
                else:
                    validate = Validate(config.sdk_config)
                    output_string, exception = validate.validate_format_result(config, output)
                    w.write(output_string)
                    if exception is not None:
                        validate_error_list.append(ValidationError(str(input_file), exception))
            else:
                warning_message = (
                    f"Skipped a query from file {input_file!s}. "
                    f"Check for unsupported operations related to STREAM, TASK, SESSION etc."
                )
                logger.warning(warning_message)

    return no_of_sqls, parse_error_list, validate_error_list


def process_directory(config: MorphConfig, root: str | Path, base_root: str, files: list[str]):
    output_folder = config.output_folder
    parse_error_list = []
    validate_error_list = []
    counter = 0

    root = Path(root)

    for file in files:
        if is_sql_file(file):
            if output_folder in (None, "None"):
                output_folder_base = root / "transpiled"
            else:
                output_folder_base = f'{output_folder.rstrip("/")}/{base_root}'

            output_file_name = Path(output_folder_base) / Path(file).name
            make_dir(output_folder_base)

            input_file = root / file

            no_of_sqls, parse_error, validation_error = process_file(config, input_file, output_file_name)
            counter = counter + no_of_sqls
            parse_error_list.extend(parse_error)
            validate_error_list.extend(validation_error)
        else:
            # Only SQL files are processed with extension .sql or .ddl
            pass

    return counter, parse_error_list, validate_error_list


def process_recursive_dirs(config: MorphConfig):
    input_sql = Path(config.input_sql)
    parse_error_list = []
    validate_error_list = []

    file_list = []
    counter = 0
    for root, _, files in dir_walk(input_sql):
        base_root = str(root).replace(str(input_sql), "")
        folder = str(input_sql.resolve().joinpath(base_root))
        msg = f"Processing for sqls under this folder: {folder}"
        logger.info(msg)
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
    input_sql = Path(config.input_sql)
    skip_validation = config.skip_validation
    status = []
    result = MorphStatus([], 0, 0, 0, [])

    if input_sql.is_file():
        if is_sql_file(input_sql):
            msg = f"Processing for sqls under this file: {input_sql}"
            logger.info(msg)
            if config.output_folder in (None, "None"):
                output_folder = input_sql.parent / "transpiled"
            else:
                output_folder = Path(config.output_folder.rstrip("/"))

            make_dir(output_folder)
            output_file = output_folder / input_sql.name
            no_of_sqls, parse_error, validation_error = process_file(config, input_sql, output_file)
            error_log = parse_error + validation_error
            result = MorphStatus([str(input_sql)], no_of_sqls, len(parse_error), len(validation_error), error_log)
        else:
            msg = f"{input_sql} is not a SQL file."
            logger.warning(msg)
    elif input_sql.is_dir():
        result = process_recursive_dirs(config)
    else:
        msg = f"{input_sql} does not exist."
        logger.error(msg)
        raise FileNotFoundError(msg)

    parse_error_count = result.parse_error_count
    validate_error_count = result.validate_error_count

    error_list_count = parse_error_count + validate_error_count

    if not skip_validation:
        logger.info(f"No of Sql Failed while Validating: {validate_error_count}")

    if error_list_count > 0:
        error_log_file = Path.cwd() / f"err_{os.getpid()}.lst"
        with error_log_file.open("a") as e:
            e.writelines(f"{err}\n" for err in result.error_log_list)
    else:
        error_log_file = "None"

    status.append(
        {
            "total_files_processed": len(result.file_list),
            "total_queries_processed": result.no_of_queries,
            "no_of_sql_failed_while_parsing": parse_error_count,
            "no_of_sql_failed_while_validating": validate_error_count,
            "error_log_file": str(error_log_file),
        }
    )
    return status
