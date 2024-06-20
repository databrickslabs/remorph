import logging
import os
from pathlib import Path

from sqlglot.dialects.dialect import Dialect
from databricks.labs.remorph.__about__ import __version__
from databricks.labs.remorph.config import (
    MorphConfig,
    get_dialect,
    TranspilationResult,
    ValidationResult,
)
from databricks.labs.remorph.helpers import db_sql
from databricks.labs.remorph.helpers.execution_time import timeit
from databricks.labs.remorph.helpers.file_utils import (
    dir_walk,
    is_sql_file,
    make_dir,
    remove_bom,
)
from databricks.labs.remorph.helpers.morph_status import (
    MorphStatus,
    ParserError,
    ValidationError,
)
from databricks.labs.remorph.helpers.validation import Validator
from databricks.labs.remorph.snow import lca_utils
from databricks.labs.remorph.snow.sql_transpiler import SqlglotEngine
from databricks.sdk import WorkspaceClient

# pylint: disable=unspecified-encoding

logger = logging.getLogger(__name__)


def _process_file(
    config: MorphConfig,
    validator: Validator | None,
    transpiler: SqlglotEngine,
    input_file: str | Path,
    output_file: str | Path,
):
    logger.info(f"started processing for the file ${input_file}")
    validate_error_list = []
    no_of_sqls = 0

    input_file = Path(input_file)
    output_file = Path(output_file)

    with input_file.open("r") as f:
        sql = remove_bom(f.read())

    lca_error = lca_utils.check_for_unsupported_lca(get_dialect(config.source.lower()), sql, str(input_file))

    if lca_error:
        validate_error_list.append(lca_error)

    write_dialect = config.get_write_dialect()

    transpiler_result: TranspilationResult = _parse(transpiler, write_dialect, sql, input_file, [])

    with output_file.open("w") as w:
        for output in transpiler_result.transpiled_sql:
            if output:
                no_of_sqls = no_of_sqls + 1
                if config.skip_validation:
                    w.write(output)
                    w.write("\n;\n")
                elif validator:
                    validation_result: ValidationResult = _validation(validator, config, output)
                    w.write(validation_result.validated_sql)
                    if validation_result.exception_msg is not None:
                        validate_error_list.append(ValidationError(str(input_file), validation_result.exception_msg))
            else:
                warning_message = (
                    f"Skipped a query from file {input_file!s}. "
                    f"Check for unsupported operations related to STREAM, TASK, SESSION etc."
                )
                logger.warning(warning_message)

    return no_of_sqls, transpiler_result.parse_error_list, validate_error_list


def _process_directory(
    config: MorphConfig,
    validator: Validator | None,
    transpiler: SqlglotEngine,
    root: str | Path,
    base_root: str,
    files: list[str],
):
    output_folder = config.output_folder
    parse_error_list = []
    validate_error_list = []
    counter = 0

    root = Path(root)

    for file in files:
        logger.info(f"Processing file :{file}")
        if is_sql_file(file):
            if output_folder in {None, "None"}:
                output_folder_base = f"{root.name}/transpiled"
            else:
                output_folder_base = f'{str(output_folder).rstrip("/")}/{base_root}'

            output_file_name = Path(output_folder_base) / Path(file).name
            make_dir(output_folder_base)

            no_of_sqls, parse_error, validation_error = _process_file(
                config, validator, transpiler, file, output_file_name
            )
            counter = counter + no_of_sqls
            parse_error_list.extend(parse_error)
            validate_error_list.extend(validation_error)
        else:
            # Only SQL files are processed with extension .sql or .ddl
            pass

    return counter, parse_error_list, validate_error_list


def _process_recursive_dirs(
    config: MorphConfig, input_sql_path: Path, validator: Validator | None, transpiler: SqlglotEngine
):
    input_sql = input_sql_path
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
        no_of_sqls, parse_error, validation_error = _process_directory(
            config, validator, transpiler, root, base_root, files
        )
        counter = counter + no_of_sqls
        parse_error_list.extend(parse_error)
        validate_error_list.extend(validation_error)

    error_log = parse_error_list + validate_error_list

    return MorphStatus(file_list, counter, len(parse_error_list), len(validate_error_list), error_log)


@timeit
def morph(workspace_client: WorkspaceClient, config: MorphConfig):
    """
    [Experimental] Transpiles the SQL queries from one dialect to another.

    :param config: The configuration for the morph operation.
    :param workspace_client: The WorkspaceClient object.
    """
    if not config.input_sql:
        logger.error("Input SQL path is not provided.")
        raise ValueError("Input SQL path is not provided.")

    input_sql = Path(config.input_sql)
    status = []
    result = MorphStatus([], 0, 0, 0, [])

    read_dialect = config.get_read_dialect()
    transpiler = SqlglotEngine(read_dialect)
    validator = None
    if not config.skip_validation:
        sql_backend = db_sql.get_sql_backend(workspace_client)
        logger.info(f"SQL Backend used for query validation: {type(sql_backend).__name__}")
        validator = Validator(sql_backend)

    if input_sql.is_file():
        if is_sql_file(input_sql):
            msg = f"Processing for sqls under this file: {input_sql}"
            logger.info(msg)
            if config.output_folder in {None, "None"}:
                output_folder = input_sql.parent / "transpiled"
            else:
                output_folder = Path(str(config.output_folder).rstrip("/"))

            make_dir(output_folder)
            output_file = output_folder / input_sql.name
            no_of_sqls, parse_error, validation_error = _process_file(
                config, validator, transpiler, input_sql, output_file
            )
            error_log = parse_error + validation_error
            result = MorphStatus([str(input_sql)], no_of_sqls, len(parse_error), len(validation_error), error_log)
        else:
            msg = f"{input_sql} is not a SQL file."
            logger.warning(msg)
    elif input_sql.is_dir():
        result = _process_recursive_dirs(config, input_sql, validator, transpiler)
    else:
        msg = f"{input_sql} does not exist."
        logger.error(msg)
        raise FileNotFoundError(msg)

    error_list_count = result.parse_error_count + result.validate_error_count
    if not config.skip_validation:
        logger.info(f"No of Sql Failed while Validating: {result.validate_error_count}")

    error_log_file = "None"
    if error_list_count > 0:
        error_log_file = str(Path.cwd().joinpath(f"err_{os.getpid()}.lst"))
        if result.error_log_list:
            with Path(error_log_file).open("a") as e:
                e.writelines(f"{err}\n" for err in result.error_log_list)

    status.append(
        {
            "total_files_processed": len(result.file_list),
            "total_queries_processed": result.no_of_queries,
            "no_of_sql_failed_while_parsing": result.parse_error_count,
            "no_of_sql_failed_while_validating": result.validate_error_count,
            "error_log_file": str(error_log_file),
        }
    )
    return status


def verify_workspace_client(workspace_client: WorkspaceClient) -> WorkspaceClient:
    # pylint: disable=protected-access
    """
    [Private] Verifies and updates the workspace client configuration.

    TODO: In future refactor this function so it can be used for reconcile module without cross access.
    """
    if workspace_client.config._product != "remorph":
        workspace_client.config._product = "remorph"
    if workspace_client.config._product_version != __version__:
        workspace_client.config._product_version = __version__
    return workspace_client


def _parse(
    transpiler: SqlglotEngine,
    write_dialect: Dialect,
    sql: str,
    input_file: str | Path,
    error_list: list[ParserError],
) -> TranspilationResult:
    return transpiler.transpile(write_dialect, sql, str(input_file), error_list)


def _validation(
    validator: Validator,
    config: MorphConfig,
    sql: str,
) -> ValidationResult:
    return validator.validate_format_result(config, sql)


@timeit
def morph_sql(
    workspace_client: WorkspaceClient,
    config: MorphConfig,
    sql: str,
) -> tuple[TranspilationResult, ValidationResult | None]:
    """[Experimental] Transpile a single SQL query from one dialect to another."""
    ws_client: WorkspaceClient = verify_workspace_client(workspace_client)

    read_dialect: Dialect = config.get_read_dialect()
    write_dialect: Dialect = config.get_write_dialect()
    transpiler: SqlglotEngine = SqlglotEngine(read_dialect)

    transpiler_result = _parse(transpiler, write_dialect, sql, "inline_sql", [])

    if not config.skip_validation:
        sql_backend = db_sql.get_sql_backend(ws_client)
        logger.info(f"SQL Backend used for query validation: {type(sql_backend).__name__}")
        validator = Validator(sql_backend)
        return transpiler_result, _validation(validator, config, transpiler_result.transpiled_sql[0])

    return transpiler_result, None


@timeit
def morph_column_exp(
    workspace_client: WorkspaceClient,
    config: MorphConfig,
    expressions: list[str],
) -> list[tuple[TranspilationResult, ValidationResult | None]]:
    """[Experimental] Transpile a list of SQL expressions from one dialect to another."""
    config.skip_validation = True
    result = []
    for sql in expressions:
        result.append(morph_sql(workspace_client, config, sql))
    return result
