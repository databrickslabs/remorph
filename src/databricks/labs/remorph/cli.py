import asyncio
import dataclasses
import json
import os
import time
from pathlib import Path

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


def raise_validation_exception(msg: str) -> Exception:
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
    logger.debug(f"Application transpiler config: {ctx.transpile_config}")
    checker = _TranspileConfigChecker(ctx.transpile_config)
    checker.use_transpiler_config_path(transpiler_config_path)
    checker.use_source_dialect(source_dialect)
    checker.use_input_source(input_source)
    checker.use_output_folder(output_folder)
    checker.use_error_file_path(error_file_path)
    checker.use_skip_validation(skip_validation)
    checker.use_catalog_name(catalog_name)
    checker.use_schema_name(schema_name)
    config, engine = checker.check()
    asyncio.run(_transpile(ctx, config, engine))


class _TranspileConfigChecker:

    def __init__(self, config: TranspileConfig | None):
        if not config:
            raise SystemExit("Installed transpile config not found. Please install Remorph transpile first.")
        self._config: TranspileConfig = config

    def use_transpiler_config_path(self, transpiler_config_path: str | None):
        if transpiler_config_path and transpiler_config_path != "None":
            logger.debug(f"Setting transpiler_config_path to '{transpiler_config_path}'")
            self._config = dataclasses.replace(self._config, transpiler_config_path=transpiler_config_path)

    def use_source_dialect(self, source_dialect: str | None):
        if source_dialect and source_dialect != "None":
            logger.debug(f"Setting source_dialect to '{source_dialect}'")
            self._config = dataclasses.replace(self._config, source_dialect=source_dialect)

    def use_input_source(self, input_source: str | None):
        if input_source and input_source != "None":
            logger.debug(f"Setting input_source to '{input_source}'")
            self._config = dataclasses.replace(self._config, input_source=input_source)

    def use_output_folder(self, output_folder: str | None):
        if output_folder and output_folder != "None":
            logger.debug(f"Setting output_folder to '{output_folder}'")
            self._config = dataclasses.replace(self._config, output_folder=output_folder)

    def use_error_file_path(self, error_file_path: str | None):
        if error_file_path and error_file_path != "None":
            logger.debug(f"Setting error_file_path to '{error_file_path}'")
            self._config = dataclasses.replace(self._config, error_file_path=error_file_path)

    def use_skip_validation(self, skip_validation: str | None):
        if skip_validation and skip_validation != "None":
            if skip_validation.lower() not in {"true", "false"}:
                raise_validation_exception(
                    f"Invalid value for '--skip-validation': '{skip_validation}' is not one of 'true', 'false'."
                )
            logger.debug(f"Setting skip_validation to '{skip_validation}'")
            self._config = dataclasses.replace(self._config, skip_validation=skip_validation.lower() == "true")

    def use_catalog_name(self, catalog_name: str | None):
        if catalog_name and catalog_name != "None":
            logger.debug(f"Setting catalog_name to '{catalog_name}'")
            self._config = dataclasses.replace(self._config, catalog_name=catalog_name)

    def use_schema_name(self, schema_name: str | None):
        if schema_name and schema_name != "None":
            logger.debug(f"Setting schema_name to '{schema_name}'")
            self._config = dataclasses.replace(self._config, schema_name=schema_name)

    def check(self) -> tuple[TranspileConfig, TranspileEngine]:
        logger.debug(f"Checking config: {self!s}")
        # not using os.path.exists because it sometimes fails mysteriously...
        if not self._config.transpiler_config_path or not Path(self._config.transpiler_config_path).exists():
            raise_validation_exception(
                f"Invalid value for '--transpiler-config-path': Path '{self._config.transpiler_config_path}' does not exist."
            )
        engine = TranspileEngine.load_engine(Path(self._config.transpiler_config_path))
        engine.check_source_dialect(self._config.source_dialect)
        if not self._config.input_source or not os.path.exists(self._config.input_source):
            raise_validation_exception(
                f"Invalid value for '--input-source': Path '{self._config.input_source}' does not exist."
            )
        # 'transpiled' will be used as output_folder if not specified
        # 'errors.log' will be used as errors file if not specified
        return self._config, engine


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
def generate_lineage(w: WorkspaceClient, source_dialect: str, input_source: str, output_folder: str):
    """[Experimental] Generates a lineage of source SQL files or folder"""
    ctx = ApplicationContext(w)
    logger.debug(f"User: {ctx.current_user}")
    engine = SqlglotEngine()
    engine.check_source_dialect(source_dialect)
    if not input_source or not os.path.exists(input_source):
        raise_validation_exception(f"Invalid value for '--input-source': Path '{input_source}' does not exist.")
    if not os.path.exists(output_folder) or output_folder in {None, ""}:
        raise_validation_exception(f"Invalid value for '--output-folder': Path '{output_folder}' does not exist.")

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
def configure_database_profiler():
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
def configure_reconcile(w: WorkspaceClient):
    """Configure the Remorph Reconcile Package"""
    with_user_agent_extra("cmd", "configure-reconcile")
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
