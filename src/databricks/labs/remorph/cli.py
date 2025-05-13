import asyncio
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

from databricks.labs.remorph.__about__ import __version__
from databricks.labs.remorph.assessments.configure_assessment import ConfigureAssessment
from databricks.labs.remorph.config import TranspileConfig
from databricks.labs.remorph.connections.credential_manager import create_credential_manager
from databricks.labs.remorph.connections.env_getter import EnvGetter
from databricks.labs.remorph.contexts.application import ApplicationContext
from databricks.labs.remorph.helpers.recon_config_utils import ReconConfigPrompts
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
    transpiler_config_path: str,
    source_dialect: str,
    input_source: str,
    output_folder: str | None,
    error_file_path: str | None,
    skip_validation: str,
    catalog_name: str,
    schema_name: str,
):
    """Transpiles source dialect to databricks dialect"""
    with_user_agent_extra("cmd", "execute-transpile")
    ctx = ApplicationContext(w)
    logger.debug(f"User: {ctx.current_user}")
    default_config = ctx.transpile_config
    if not default_config:
        raise SystemExit("Installed transpile config not found. Please install Remorph transpile first.")
    _override_workspace_client_config(ctx, default_config.sdk_config)
    engine = TranspileEngine.load_engine(Path(transpiler_config_path))
    engine.check_source_dialect(source_dialect)
    if not input_source or not os.path.exists(input_source):
        raise_validation_exception(f"Invalid value for '--input-source': Path '{input_source}' does not exist.")
    if not output_folder and default_config.output_folder:
        output_folder = str(default_config.output_folder)
    if not error_file_path and default_config.error_file_path:
        error_file_path = str(default_config.error_file_path)
    if skip_validation.lower() not in {"true", "false"}:
        raise_validation_exception(
            f"Invalid value for '--skip-validation': '{skip_validation}' is not one of 'true', 'false'."
        )

    sdk_config = default_config.sdk_config if default_config.sdk_config else None
    catalog_name = catalog_name if catalog_name else default_config.catalog_name
    schema_name = schema_name if schema_name else default_config.schema_name

    config = TranspileConfig(
        transpiler_config_path=transpiler_config_path,
        source_dialect=source_dialect.lower(),
        input_source=input_source,
        output_folder=output_folder,
        error_file_path=error_file_path,
        skip_validation=skip_validation.lower() == "true",  # convert to bool
        catalog_name=catalog_name,
        schema_name=schema_name,
        sdk_config=sdk_config,
    )
    status, errors = asyncio.run(do_transpile(ctx.workspace_client, engine, config))

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
    logger.debug(f"User: {ctx.current_user}")
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
    logger.debug(f"User: {ctx.current_user}")
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
def install_assessment():
    """Install the Remorph Assessment package"""
    prompts = Prompts()
    credential = create_credential_manager("remorph", EnvGetter())
    assessment = ConfigureAssessment(product_name="remorph", prompts=prompts)
    assessment.run(cred_manager=credential)


@remorph.command()
def install_transpile(w: WorkspaceClient):
    """Install the Remorph Transpile package"""
    with_user_agent_extra("cmd", "install-transpile")
    installer = _installer(w)
    installer.run(module="transpile")


@remorph.command(is_unauthenticated=False)
def install_reconcile(w: WorkspaceClient):
    """Install the Remorph Reconcile package"""
    with_user_agent_extra("cmd", "install-reconcile")
    dbsql_id = _create_warehouse(w)
    w.config.warehouse_id = dbsql_id
    installer = _installer(w)
    installer.run(module="reconcile")
    _remove_warehouse(w, dbsql_id)


@remorph.command()
def analyze(w: WorkspaceClient):
    """Run the Analyzer"""
    with_user_agent_extra("cmd", "analyze")
    ctx = ApplicationContext(w)
    prompts = ctx.prompts
    output_folder = prompts.question("Enter path to output results folder")
    input_folder = prompts.question("Enter path to input sources folder")
    source_tech = prompts.choice("Select the source technology", Analyzer.supported_source_technologies())
    with_user_agent_extra("analyzer_source_tech", source_tech)
    Analyzer.analyze(Path(input_folder), Path(output_folder), source_tech)


if __name__ == "__main__":
    remorph()
