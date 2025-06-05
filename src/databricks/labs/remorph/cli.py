import asyncio
import dataclasses
import json
import os
import time
from pathlib import Path
from typing import NoReturn

from databricks.sdk.core import with_user_agent_extra
from databricks.sdk.service.sql import CreateWarehouseRequestWarehouseType
from databricks.sdk import WorkspaceClient

from databricks.labs.blueprint.cli import App
from databricks.labs.blueprint.entrypoint import get_logger
from databricks.labs.blueprint.tui import Prompts

from databricks.labs.bladespector.analyzer import Analyzer


from databricks.labs.remorph.assessments.configure_assessment import (
    create_assessment_configurator,
    PROFILER_SOURCE_SYSTEM,
)

from databricks.labs.remorph.__about__ import __version__

from databricks.labs.remorph.config import TranspileConfig
from databricks.labs.remorph.contexts.application import ApplicationContext
from databricks.labs.remorph.helpers.recon_config_utils import ReconConfigPrompts
from databricks.labs.remorph.helpers.telemetry_utils import make_alphanum_or_semver
from databricks.labs.remorph.install import WorkspaceInstaller
from databricks.labs.remorph.lineage import lineage_generator
from databricks.labs.remorph.reconcile.runner import ReconcileRunner
from databricks.labs.remorph.reconcile.recon_config import RECONCILE_OPERATION_NAME, AGG_RECONCILE_OPERATION_NAME
from databricks.labs.remorph.transpiler.execute import transpile as do_transpile
from databricks.labs.remorph.transpiler.sqlglot.sqlglot_engine import SqlglotEngine
from databricks.labs.remorph.transpiler.transpile_engine import TranspileEngine


remorph = App(__file__)
logger = get_logger(__file__)


def raise_validation_exception(msg: str) -> NoReturn:
    raise ValueError(msg)


def _installer(ws: WorkspaceClient) -> WorkspaceInstaller:
    app_context = ApplicationContext(_verify_workspace_client(ws))
    return WorkspaceInstaller(
        app_context.workspace_client,
        app_context.prompts,
        app_context.installation,
        app_context.install_state,
        app_context.product_info,
        app_context.resource_configurator,
        app_context.workspace_installation,
    )


def _create_warehouse(ws: WorkspaceClient) -> str:

    dbsql = ws.warehouses.create_and_wait(
        name=f"remorph-warehouse-{time.time_ns()}",
        warehouse_type=CreateWarehouseRequestWarehouseType.PRO,
        cluster_size="Small",  # Adjust size as needed
        auto_stop_mins=30,  # Auto-stop after 30 minutes of inactivity
        enable_serverless_compute=True,
        max_num_clusters=1,
    )

    if dbsql.id is None:
        raise RuntimeError(f"Failed to create warehouse {dbsql.name}")

    logger.info(f"Created warehouse with id: {dbsql.id}")
    return dbsql.id


def _remove_warehouse(ws: WorkspaceClient, warehouse_id: str):
    ws.warehouses.delete(warehouse_id)
    logger.info(f"Removed warehouse post installation with id: {warehouse_id}")


def _verify_workspace_client(ws: WorkspaceClient) -> WorkspaceClient:
    """
    [Private] Verifies and updates the workspace client configuration.
    """

    # Using reflection to set right value for _product_info for telemetry
    product_info = getattr(ws.config, '_product_info')
    if product_info[0] != "remorph":
        setattr(ws.config, '_product_info', ('remorph', __version__))

    return ws


@remorph.command
def transpile(
    w: WorkspaceClient,
    transpiler_config_path: str | None = None,
    source_dialect: str | None = None,
    input_source: str | None = None,
    output_folder: str | None = None,
    error_file_path: str | None = None,
    skip_validation: str | None = None,
    catalog_name: str | None = None,
    schema_name: str | None = None,
):
    """Transpiles source dialect to databricks dialect"""
    ctx = ApplicationContext(w)
    logger.debug(f"Preconfigured transpiler config: {ctx.transpile_config!r}")
    checker = _TranspileConfigChecker(ctx.transpile_config)
    # Warning: the order of these calls matters: transpiler config path must be set before the source dialect.
    checker.use_transpiler_config_path(transpiler_config_path)
    checker.use_source_dialect(source_dialect)
    checker.use_input_source(input_source)
    checker.use_output_folder(output_folder)
    checker.use_error_file_path(error_file_path)
    checker.use_skip_validation(skip_validation)
    checker.use_catalog_name(catalog_name)
    checker.use_schema_name(schema_name)
    config, engine = checker.check()
    logger.debug(f"Final configuration for transpilation: {config!r}")
    asyncio.run(_transpile(ctx, config, engine))


class _TranspileConfigChecker:
    """Helper class for the 'transpile' command to check and consolidate the configuration."""

    #
    # Conventions in this class:
    #
    #  - When a command-line override is provided, we:
    #     - Log that the override is being set (at DEBUG level).
    #     - Validate it immediately, with any error message mentioning the command-line argument.
    #     - Only update the configuration if the validation passes.
    #  - With the exception of the transpiler config path and source dialect, order of overrides does not matter.
    #  - The final .check() must _again_ check all arguments and validate them again.
    #     - If missing, the error must indicate that the command-line argument is missing.
    #     - If invalid, we know that the config file has an invalid value. (Overrides were already validated.)
    #
    # This ensures that we distinguish between:
    #  - Missing configuration that isn't in the configuration or provided via the command-line.
    #    Resolution: provide the missing command-line argument.
    #  - Invalid command-line arguments:
    #    Resolution: fix the command-line argument value.
    #  - Invalid configuration file values:
    #    Resolution: fix the configuration file value, or provide the command-line argument to override it.
    #
    # TODO: Refactor this class to eliminate a lof of the boilerplate and handle this more elegantly.

    _config: TranspileConfig
    """The workspace configuration for transpiling, updated from command-line arguments."""
    _engine: TranspileEngine | None
    """The transpiler engine to use for transpiling, lazily loaded based on the configuration."""

    def __init__(self, config: TranspileConfig | None) -> None:
        if config is None:
            # TODO: Remove this; it triggers an immediate exit from Python. Return gracefully instead.
            raise SystemExit("Installed transpile config not found. Please install Remorph transpile first.")
        self._config = config
        self._engine = None

    def use_transpiler_config_path(self, transpiler_config_path: str | None) -> None:
        if transpiler_config_path is not None:
            # If the engine has already been loaded, it means the source dialect was set before this method was called.
            # That's a bug in the code, as the transpiler config path should be set before the source dialect.
            assert self._engine is None, "Transpiler path changed after source dialect was set."
            logger.debug(f"Setting transpiler_config_path to: {transpiler_config_path!r}")
            if not Path(transpiler_config_path).exists():
                msg = f"Invalid path for '--transpiler-config-path', does not exist: {transpiler_config_path}"
                raise_validation_exception(msg)
            self._config = dataclasses.replace(self._config, transpiler_config_path=transpiler_config_path)

    @property
    def _transpiler_config_path(self) -> Path:
        # Path for the transpiler config file cannot be missing, it's mandatory on the config.
        config_path = Path(self._config.transpiler_config_path)
        if not config_path.exists():
            msg = f"Invalid transpiler configuration path, does not exist: {config_path}"
            raise_validation_exception(msg)
        return config_path

    def _load_engine(self) -> TranspileEngine:
        engine = self._engine
        if engine is None:
            engine = TranspileEngine.load_engine(self._transpiler_config_path)
            self._engine = engine
        return engine

    def use_source_dialect(self, source_dialect: str | None) -> None:
        if source_dialect is not None:
            logger.debug(f"Setting source_dialect to: {source_dialect!r}")
            engine = self._load_engine()
            if source_dialect not in engine.supported_dialects:
                supported_dialects_description = ", ".join(engine.supported_dialects)
                msg = f"Unsupported source dialect provided for '--source-dialect': {source_dialect!r} (supported: {supported_dialects_description})"
                raise_validation_exception(msg)
            self._config = dataclasses.replace(self._config, source_dialect=source_dialect)

    def use_input_source(self, input_source: str | None) -> None:
        if input_source is not None:
            logger.debug(f"Setting input_source to: {input_source!r}")
            if not Path(input_source).exists():
                raise_validation_exception(f"Invalid path for '--input-source', does not exist: {input_source}")
            self._config = dataclasses.replace(self._config, input_source=input_source)

    def use_output_folder(self, output_folder: str | None) -> None:
        if output_folder is not None:
            logger.debug(f"Setting output_folder to: {output_folder!r}")
            if not Path(output_folder).parent.exists():
                raise_validation_exception(
                    f"Invalid path for '--output-folder', parent does not exist: {output_folder}"
                )
            self._config = dataclasses.replace(self._config, output_folder=output_folder)

    def use_error_file_path(self, error_file_path: str | None) -> None:
        if error_file_path is not None:
            logger.debug(f"Setting error_file_path to: {error_file_path!r}")
            if not Path(error_file_path).parent.exists():
                raise_validation_exception(
                    f"Invalid path for '--error-file-path', parent does not exist: {error_file_path}"
                )
            self._config = dataclasses.replace(self._config, error_file_path=error_file_path)

    def use_skip_validation(self, skip_validation: str | None) -> None:
        if skip_validation is not None:
            skip_validation_lower = skip_validation.lower()
            if skip_validation_lower not in {"true", "false"}:
                msg = f"Invalid value for '--skip-validation': {skip_validation!r} must be 'true' or 'false'."
                raise_validation_exception(msg)
            new_skip_validation = skip_validation_lower == "true"
            logger.debug(f"Setting skip_validation to: {new_skip_validation!r}")
            self._config = dataclasses.replace(self._config, skip_validation=new_skip_validation)

    def use_catalog_name(self, catalog_name: str | None) -> None:
        if catalog_name:
            logger.debug(f"Setting catalog_name to: {catalog_name!r}")
            self._config = dataclasses.replace(self._config, catalog_name=catalog_name)

    def use_schema_name(self, schema_name: str | None) -> None:
        if schema_name:
            logger.debug(f"Setting schema_name to: {schema_name!r}")
            self._config = dataclasses.replace(self._config, schema_name=schema_name)

    def check(self) -> tuple[TranspileConfig, TranspileEngine]:
        """Checks that all configuration parameters are present and valid."""
        config = self._config
        logger.debug(f"Checking config: {config!r}")

        # Input source path must be provided and exist.
        config_input_source = config.input_source
        if config_input_source is None:
            raise_validation_exception("Missing input source path, specify with '--input-source'.")
        if not Path(config_input_source).exists():
            raise_validation_exception(f"Invalid input source path configured, does not exist: {config_input_source}")

        # Output folder must be provided, and its parent must exist.
        config_output_folder = config.output_folder
        if config_output_folder is None:
            raise_validation_exception("Missing output path, specify with '--output-folder'.")
        if not Path(config_output_folder).parent.exists():
            msg = f"Invalid output folder configured, parent does not exist for: {config_output_folder}"
            raise_validation_exception(msg)

        # If provided, the error file path must be valid. (It's optional though.)
        config_error_file_path = config.error_file_path
        if config_error_file_path is not None and not Path(config_error_file_path).parent.exists():
            msg = f"Invalid error file path configured, parent does not exist for: {config_error_file_path}"
            raise_validation_exception(msg)

        # Check the source dialect against the transpiler engine.
        config_source_dialect = config.source_dialect
        if config_source_dialect is None:
            raise_validation_exception("Missing source dialect, specify with '--source-dialect'.")
        engine = self._load_engine()
        if config_source_dialect not in engine.supported_dialects:
            supported_dialects_description = ", ".join(engine.supported_dialects)
            msg = f"Unsupported source dialect configured: {config_source_dialect!r} (supported: {supported_dialects_description})"
            raise_validation_exception(msg)

        # Skip validation must be on the config; no validation required.
        # catalog_name and schema_name are mandatory, but not currently validated.
        # TODO: If validation is happening, we should check that the catalog and schema names are valid.

        return config, engine


async def _transpile(ctx: ApplicationContext, config: TranspileConfig, engine: TranspileEngine):
    """Transpiles source dialect to databricks dialect"""
    with_user_agent_extra("cmd", "execute-transpile")
    user = ctx.current_user
    logger.debug(f"User: {user}")
    _override_workspace_client_config(ctx, config.sdk_config)
    status, errors = await do_transpile(ctx.workspace_client, engine, config)
    for error in errors:
        logger.error(f"Error Transpiling: {str(error)}")

    # Table Template in labs.yml requires the status to be list of dicts Do not change this
    print(json.dumps([status]))


def _override_workspace_client_config(ctx: ApplicationContext, overrides: dict[str, str] | None):
    """
    Override the Workspace client's SDK config with the user provided SDK config.
    Users can provide the cluster_id and warehouse_id during the installation.
    This will update the default config object in-place.
    """
    if not overrides:
        return

    warehouse_id = overrides.get("warehouse_id")
    if warehouse_id:
        ctx.connect_config.warehouse_id = warehouse_id

    cluster_id = overrides.get("cluster_id")
    if cluster_id:
        ctx.connect_config.cluster_id = cluster_id


@remorph.command
def reconcile(w: WorkspaceClient):
    """[EXPERIMENTAL] Reconciles source to Databricks datasets"""
    with_user_agent_extra("cmd", "execute-reconcile")
    ctx = ApplicationContext(w)
    user = ctx.current_user
    logger.debug(f"User: {user}")
    recon_runner = ReconcileRunner(
        ctx.workspace_client,
        ctx.installation,
        ctx.install_state,
        ctx.prompts,
    )
    recon_runner.run(operation_name=RECONCILE_OPERATION_NAME)


@remorph.command
def aggregates_reconcile(w: WorkspaceClient):
    """[EXPERIMENTAL] Reconciles Aggregated source to Databricks datasets"""
    with_user_agent_extra("cmd", "execute-aggregates-reconcile")
    ctx = ApplicationContext(w)
    user = ctx.current_user
    logger.debug(f"User: {user}")
    recon_runner = ReconcileRunner(
        ctx.workspace_client,
        ctx.installation,
        ctx.install_state,
        ctx.prompts,
    )

    recon_runner.run(operation_name=AGG_RECONCILE_OPERATION_NAME)


@remorph.command
def generate_lineage(w: WorkspaceClient, *, source_dialect: str | None = None, input_source: str, output_folder: str):
    """[Experimental] Generates a lineage of source SQL files or folder"""
    ctx = ApplicationContext(w)
    logger.debug(f"User: {ctx.current_user}")
    if not os.path.exists(input_source):
        raise_validation_exception(f"Invalid path for '--input-source': Path '{input_source}' does not exist.")
    if not os.path.exists(output_folder):
        raise_validation_exception(f"Invalid path for '--output-folder': Path '{output_folder}' does not exist.")
    if source_dialect is None:
        raise_validation_exception("Value for '--source-dialect' must be provided.")
    engine = SqlglotEngine()
    supported_dialects = engine.supported_dialects
    if source_dialect not in supported_dialects:
        supported_dialects_description = ", ".join(supported_dialects)
        msg = f"Unsupported source dialect provided for '--source-dialect': '{source_dialect}' (supported: {supported_dialects_description})"
        raise_validation_exception(msg)

    lineage_generator(engine, source_dialect, input_source, output_folder)


@remorph.command
def configure_secrets(w: WorkspaceClient):
    """Setup reconciliation connection profile details as Secrets on Databricks Workspace"""
    recon_conf = ReconConfigPrompts(w)

    # Prompt for source
    source = recon_conf.prompt_source()

    logger.info(f"Setting up Scope, Secrets for `{source}` reconciliation")
    recon_conf.prompt_and_save_connection_details()


@remorph.command(is_unauthenticated=True)
def install_assessment():
    """[Experimental] Install the Remorph Assessment package"""
    prompts = Prompts()

    # Prompt for source system
    source_system = str(
        prompts.choice("Please select the source system you want to configure", PROFILER_SOURCE_SYSTEM)
    ).lower()

    # Create appropriate assessment configurator
    assessment = create_assessment_configurator(source_system=source_system, product_name="remorph", prompts=prompts)
    assessment.run()


@remorph.command()
def install_transpile(w: WorkspaceClient, artifact: str | None = None):
    """Install the Remorph Transpilers"""
    with_user_agent_extra("cmd", "install-transpile")
    user = w.current_user
    logger.debug(f"User: {user}")
    installer = _installer(w)
    installer.run(module="transpile", artifact=artifact)


@remorph.command(is_unauthenticated=False)
def install_reconcile(w: WorkspaceClient):
    """Install the Remorph Reconcile package"""
    with_user_agent_extra("cmd", "install-reconcile")
    user = w.current_user
    logger.debug(f"User: {user}")
    dbsql_id = _create_warehouse(w)
    w.config.warehouse_id = dbsql_id
    installer = _installer(w)
    installer.run(module="reconcile")
    _remove_warehouse(w, dbsql_id)


@remorph.command()
def analyze(w: WorkspaceClient, source_directory: str, report_file: str):
    """Run the Analyzer"""
    with_user_agent_extra("cmd", "analyze")
    ctx = ApplicationContext(w)
    prompts = ctx.prompts
    output_file = report_file
    input_folder = source_directory
    source_tech = prompts.choice("Select the source technology", Analyzer.supported_source_technologies())
    with_user_agent_extra("analyzer_source_tech", make_alphanum_or_semver(source_tech))
    user = ctx.current_user
    logger.debug(f"User: {user}")
    Analyzer.analyze(Path(input_folder), Path(output_file), source_tech)


if __name__ == "__main__":
    remorph()
