import asyncio
import datetime
import logging
from pathlib import Path
from typing import cast, Any

from databricks.labs.remorph.__about__ import __version__
from databricks.labs.remorph.config import (
    TranspileConfig,
    TranspileResult,
    ValidationResult,
)
from databricks.labs.remorph.helpers import db_sql
from databricks.labs.remorph.helpers.execution_time import timeit
from databricks.labs.remorph.helpers.file_utils import (
    dir_walk,
    is_sql_file,
    make_dir,
)
from databricks.labs.remorph.transpiler.transpile_engine import TranspileEngine
from databricks.labs.remorph.transpiler.transpile_status import (
    TranspileStatus,
    TranspileError,
    ErrorKind,
    ErrorSeverity,
)
from databricks.labs.remorph.helpers.string_utils import remove_bom
from databricks.labs.remorph.helpers.validation import Validator
from databricks.labs.remorph.transpiler.sqlglot.sqlglot_engine import SqlglotEngine
from databricks.sdk import WorkspaceClient

logger = logging.getLogger(__name__)


async def _process_one_file(
    config: TranspileConfig,
    validator: Validator | None,
    transpiler: TranspileEngine,
    input_path: Path,
    output_path: Path,
) -> tuple[int, list[TranspileError]]:
    logger.debug(f"Started processing file: {input_path}")
    error_list: list[TranspileError] = []

    with input_path.open("r") as f:
        source_code = remove_bom(f.read())

    transpile_result = await _transpile(
        transpiler, config.source_dialect, config.target_dialect, source_code, input_path
    )
    # Potentially expensive, only evaluate if debug is enabled
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(f"Finished transpiling file: {input_path} (result: {transpile_result})")

    error_list.extend(transpile_result.error_list)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w") as w:
        if validator:
            logger.debug(f"Validating transpiled code for file: {input_path}")
            validation_result = _validation(validator, config, transpile_result.transpiled_code)
            # Potentially expensive, only evaluate if debug is enabled
            if logger.isEnabledFor(logging.DEBUG):
                msg = f"Finished validating transpiled code for file: {input_path} (result: {validation_result})"
                logger.debug(msg)
            w.write(validation_result.validated_sql)
            if validation_result.exception_msg is not None:
                error = TranspileError(
                    "VALIDATION_ERROR",
                    ErrorKind.VALIDATION,
                    ErrorSeverity.WARNING,
                    input_path,
                    validation_result.exception_msg,
                )
                error_list.append(error)
        else:
            w.write(transpile_result.transpiled_code)
            w.write("\n;\n")

    logger.info(f"Processed file: {input_path} (errors: {len(error_list)})")
    return transpile_result.success_count, error_list


async def _process_many_files(
    config: TranspileConfig,
    validator: Validator | None,
    transpiler: TranspileEngine,
    output_folder: Path,
    files: list[Path],
) -> tuple[int, list[TranspileError]]:

    counter = 0
    all_errors: list[TranspileError] = []

    for file in files:
        logger.info(f"Processing file: {file}")
        if not is_sql_file(file) and not is_dbt_project_file(file):
            continue
        output_file_name = output_folder / file.name
        success_count, error_list = await _process_one_file(config, validator, transpiler, file, output_file_name)
        counter = counter + success_count
        all_errors.extend(error_list)

    return counter, all_errors


def is_dbt_project_file(file: Path):
    # it's ok to hardcode the file name here, see https://docs.getdbt.com/reference/dbt_project.yml
    return file.name == "dbt_project.yml"


async def _process_input_dir(config: TranspileConfig, validator: Validator | None, transpiler: TranspileEngine):
    error_list = []
    file_list = []
    counter = 0
    input_path = config.input_path
    output_folder = config.output_path
    if output_folder is None:
        output_folder = input_path.parent / "transpiled"
    make_dir(output_folder)
    for source_dir, _, files in dir_walk(input_path):
        relative_path = cast(Path, source_dir).relative_to(input_path)
        transpiled_dir = output_folder / relative_path
        logger.info(f"Transpiling sql files from folder: {source_dir!s} into {transpiled_dir!s}")
        file_list.extend(files)
        no_of_sqls, errors = await _process_many_files(config, validator, transpiler, transpiled_dir, files)
        counter = counter + no_of_sqls
        error_list.extend(errors)
    return TranspileStatus(file_list, counter, error_list)


async def _process_input_file(
    config: TranspileConfig, validator: Validator | None, transpiler: TranspileEngine
) -> TranspileStatus:
    if not is_sql_file(config.input_path):
        msg = f"{config.input_source} is not a SQL file."
        logger.warning(msg)
        # silently ignore non-sql files
        return TranspileStatus([], 0, [])
    msg = f"Transpiling sql file: {config.input_path!s}"
    logger.info(msg)
    output_path = config.output_path
    if output_path is None:
        output_path = config.input_path.parent / "transpiled"
    make_dir(output_path)
    output_file = output_path / config.input_path.name
    no_of_sqls, error_list = await _process_one_file(config, validator, transpiler, config.input_path, output_file)
    return TranspileStatus([config.input_path], no_of_sqls, error_list)


async def transpile(
    workspace_client: WorkspaceClient, engine: TranspileEngine, config: TranspileConfig
) -> tuple[dict[str, Any], list[TranspileError]]:
    await engine.initialize(config)
    status, errors = await _do_transpile(workspace_client, engine, config)
    await engine.shutdown()
    return status, errors


async def _do_transpile(
    workspace_client: WorkspaceClient, engine: TranspileEngine, config: TranspileConfig
) -> tuple[dict[str, Any], list[TranspileError]]:
    """
    [Experimental] Transpiles the SQL queries from one dialect to another.

    :param workspace_client: The WorkspaceClient object.
    :param engine: The TranspileEngine.
    :param config: The configuration for the morph operation.
    """
    if not config.input_source:
        logger.error("Input SQL path is not provided.")
        raise ValueError("Input SQL path is not provided.")

    validator = None
    if not config.skip_validation:
        sql_backend = db_sql.get_sql_backend(workspace_client)
        logger.info(f"SQL Backend used for query validation: {type(sql_backend).__name__}")
        validator = Validator(sql_backend)
    if config.input_source is None:
        raise ValueError("Missing input source!")
    if config.input_path.is_dir():
        logger.debug(f"Starting to process input directory: {config.input_path}")
        result = await _process_input_dir(config, validator, engine)
    elif config.input_path.is_file():
        logger.debug(f"Starting to process input file: {config.input_path}")
        result = await _process_input_file(config, validator, engine)
    else:
        msg = f"{config.input_source} does not exist."
        logger.error(msg)
        raise FileNotFoundError(msg)
    logger.debug(f"Transpiler results: {result}")

    if not config.skip_validation:
        logger.info(f"SQL validation errors: {result.validation_error_count}")
    
    logger.info("**********result.file_list")
    logger.info(result.file_list)

    error_log_path: Path | None = None
    if result.error_list:
        if config.error_path:
            error_log_path = config.error_path
        else:
            timestamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
            error_log_path = Path.cwd().joinpath(f"transpile_errors_{timestamp}.lst")
        with cast(Path, error_log_path).open("a", encoding="utf-8") as e:
            e.writelines(f"{err!s}\n" for err in result.error_list)
        

    status = {
        "total_files_processed": len(result.file_list),
        "total_queries_processed": result.no_of_transpiled_queries,
        "analysis_error_count": result.analysis_error_count,
        "parsing_error_count": result.parsing_error_count,
        "validation_error_count": result.validation_error_count,
        "generation_error_count": result.generation_error_count,
        "error_log_file": str(error_log_path),
    }
    logger.info("**********result.file_list")
    logger.info(result.file_list)

    return status, result.error_list


def verify_workspace_client(workspace_client: WorkspaceClient) -> WorkspaceClient:
    """
    [Private] Verifies and updates the workspace client configuration.

    TODO: In future refactor this function so it can be used for reconcile module without cross access.
    """

    # Using reflection to set right value for _product_info for telemetry
    product_info = getattr(workspace_client.config, '_product_info')
    if product_info[0] != "remorph":
        setattr(workspace_client.config, '_product_info', ('remorph', __version__))

    return workspace_client


async def _transpile(
    engine: TranspileEngine, from_dialect: str, to_dialect: str, source_code: str, input_path: Path
) -> TranspileResult:
    return await engine.transpile(from_dialect, to_dialect, source_code, input_path)


def _validation(
    validator: Validator,
    config: TranspileConfig,
    sql: str,
) -> ValidationResult:
    return validator.validate_format_result(config, sql)


@timeit
def transpile_sql(
    workspace_client: WorkspaceClient,
    config: TranspileConfig,
    source_sql: str,
) -> tuple[TranspileResult, ValidationResult | None]:
    """[Experimental] Transpile a single SQL query from one dialect to another."""
    ws_client: WorkspaceClient = verify_workspace_client(workspace_client)

    engine: TranspileEngine = SqlglotEngine()

    transpiler_result = asyncio.run(
        _transpile(engine, config.source_dialect, config.target_dialect, source_sql, Path("inline_sql"))
    )

    if config.skip_validation:
        return transpiler_result, None

    sql_backend = db_sql.get_sql_backend(ws_client)
    logger.info(f"SQL Backend used for query validation: {type(sql_backend).__name__}")
    validator = Validator(sql_backend)
    return transpiler_result, _validation(validator, config, transpiler_result.transpiled_code)


@timeit
def transpile_column_exp(
    workspace_client: WorkspaceClient,
    config: TranspileConfig,
    expressions: list[str],
) -> list[tuple[TranspileResult, ValidationResult | None]]:
    """[Experimental] Transpile a list of SQL expressions from one dialect to another."""
    config.skip_validation = True
    result = []
    for sql in expressions:
        result.append(transpile_sql(workspace_client, config, sql))
    return result
