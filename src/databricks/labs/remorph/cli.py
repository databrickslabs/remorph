import json
import os
from pathlib import Path

from databricks.labs.blueprint.cli import App
from databricks.labs.blueprint.entrypoint import get_logger
from databricks.labs.remorph.config import TranspileConfig
from databricks.labs.remorph.contexts.application import ApplicationContext
from databricks.labs.remorph.helpers.recon_config_utils import ReconConfigPrompts
from databricks.labs.remorph.reconcile.runner import ReconcileRunner
from databricks.labs.remorph.lineage import lineage_generator
from databricks.labs.remorph.transpiler.execute import transpile as do_transpile
from databricks.labs.remorph.reconcile.execute import RECONCILE_OPERATION_NAME, AGG_RECONCILE_OPERATION_NAME
from databricks.labs.remorph.jvmproxy import proxy_command

from databricks.sdk import WorkspaceClient

from databricks.labs.remorph.transpiler.sqlglot.dialect_utils import SQLGLOT_DIALECTS
from databricks.labs.remorph.transpiler.transpile_engine import TranspileEngine

remorph = App(__file__)
logger = get_logger(__file__)


def raise_validation_exception(msg: str) -> Exception:
    raise ValueError(msg)


proxy_command(remorph, "debug-script")
proxy_command(remorph, "debug-me")
proxy_command(remorph, "debug-coverage")
proxy_command(remorph, "debug-estimate")
proxy_command(remorph, "debug-bundle")


@remorph.command
def transpile(
    w: WorkspaceClient,
    transpiler: str,
    source_dialect: str | None,
    input_source: str,
    output_folder: str | None,
    skip_validation: str,
    catalog_name: str,
    schema_name: str,
    mode: str,
):
    """Transpiles source dialect to databricks dialect"""
    ctx = ApplicationContext(w)
    logger.info(f"User: {ctx.current_user}")
    default_config = ctx.transpile_config
    if not default_config:
        raise SystemExit("Installed transpile config not found. Please install Remorph transpile first.")
    _override_workspace_client_config(ctx, default_config.sdk_config)
    mode = mode if mode else "current"  # not checking for default config as it will always be current
    engine = TranspileEngine.load_engine(Path(transpiler))
    source_dialect = engine.check_source_dialect(source_dialect)
    if not input_source or not os.path.exists(input_source):
        raise_validation_exception(f"Invalid value for '--input-source': Path '{input_source}' does not exist.")
    if not output_folder and default_config.output_folder:
        output_folder = str(default_config.output_folder)
    if skip_validation.lower() not in {"true", "false"}:
        raise_validation_exception(
            f"Invalid value for '--skip-validation': '{skip_validation}' is not one of 'true', 'false'."
        )
    if mode.lower() not in {"current", "experimental"}:
        raise_validation_exception(
            f"Invalid value for '--mode': '{mode}' " f"is not one of 'current', 'experimental'."
        )

    sdk_config = default_config.sdk_config if default_config.sdk_config else None
    catalog_name = catalog_name if catalog_name else default_config.catalog_name
    schema_name = schema_name if schema_name else default_config.schema_name

    config = TranspileConfig(
        transpiler=transpiler,
        source_dialect=source_dialect.lower(),
        input_source=input_source,
        output_folder=output_folder,
        skip_validation=skip_validation.lower() == "true",  # convert to bool
        catalog_name=catalog_name,
        schema_name=schema_name,
        mode=mode,
        sdk_config=sdk_config,
    )

    status = do_transpile(ctx.workspace_client, engine, config)

    print(json.dumps(status))


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
    ctx = ApplicationContext(w)
    logger.info(f"User: {ctx.current_user}")
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
    ctx = ApplicationContext(w)
    logger.info(f"User: {ctx.current_user}")
    recon_runner = ReconcileRunner(
        ctx.workspace_client,
        ctx.installation,
        ctx.install_state,
        ctx.prompts,
    )

    recon_runner.run(operation_name=AGG_RECONCILE_OPERATION_NAME)


@remorph.command
def generate_lineage(w: WorkspaceClient, transpiler: str, source_dialect: str, input_source: str, output_folder: str):
    """[Experimental] Generates a lineage of source SQL files or folder"""
    ctx = ApplicationContext(w)
    logger.info(f"User: {ctx.current_user}")
    if transpiler.lower() != "sqlglot":
        if not Path(transpiler).exists():
            raise_validation_exception(f"Invalid value for '--transpiler': '{transpiler}', file does not exist.")
    if source_dialect.lower() not in SQLGLOT_DIALECTS:
        dialects = sorted(SQLGLOT_DIALECTS.keys())
        raise_validation_exception(
            f"Invalid value for '--source-dialect': '{source_dialect}' is not one of {dialects}."
        )
    if not input_source or not os.path.exists(input_source):
        raise_validation_exception(f"Invalid value for '--input-source': Path '{input_source}' does not exist.")
    if not os.path.exists(output_folder) or output_folder in {None, ""}:
        raise_validation_exception(
            f"Invalid value for '--output-folder': Path '{output_folder}' does not exist."
        )

    lineage_generator(source_dialect, input_source, output_folder)


@remorph.command
def configure_secrets(w: WorkspaceClient):
    """Setup reconciliation connection profile details as Secrets on Databricks Workspace"""
    recon_conf = ReconConfigPrompts(w)

    # Prompt for source
    source = recon_conf.prompt_source()

    logger.info(f"Setting up Scope, Secrets for `{source}` reconciliation")
    recon_conf.prompt_and_save_connection_details()


if __name__ == "__main__":
    remorph()
