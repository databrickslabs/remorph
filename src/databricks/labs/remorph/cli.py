import json
import os
import webbrowser

from pyspark.sql import SparkSession

from databricks.connect import DatabricksSession
from databricks.labs.blueprint.cli import App
from databricks.labs.blueprint.entrypoint import get_logger
from databricks.labs.blueprint.installation import Installation, SerdeError
from databricks.labs.remorph.config import SQLGLOT_DIALECTS, MorphConfig, ReconcileConfig, TableRecon
from databricks.labs.remorph.helpers.recon_config_utils import ReconConfigPrompts
from databricks.labs.remorph.lineage import lineage_generator
from databricks.labs.remorph.transpiler.execute import morph
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import NotFound
from databricks.sdk.errors import PermissionDenied
from databricks.labs.blueprint.tui import Prompts


remorph = App(__file__)
logger = get_logger(__file__)

DIALECTS = {name for name, dialect in SQLGLOT_DIALECTS.items()}


def raise_validation_exception(msg: str) -> Exception:
    raise ValueError(msg)


@remorph.command
def transpile(
    w: WorkspaceClient,
    source: str,
    input_sql: str,
    output_folder: str | None,
    skip_validation: str,
    catalog_name: str,
    schema_name: str,
    mode: str,
):
    """transpiles source dialect to databricks dialect"""
    logger.info(f"user: {w.current_user.me()}")
    installation = Installation.current(w, 'remorph')
    default_config = installation.load(MorphConfig)
    mode = mode if mode else "current"  # not checking for default config as it will always be current

    if source.lower() not in SQLGLOT_DIALECTS:
        raise_validation_exception(f"Error: Invalid value for '--source': '{source}' is not one of {DIALECTS}. ")
    if not os.path.exists(input_sql) or input_sql in {None, ""}:
        raise_validation_exception(f"Error: Invalid value for '--input_sql': Path '{input_sql}' does not exist.")
    if not output_folder:
        output_folder = default_config.output_folder if default_config.output_folder else None
    if skip_validation.lower() not in {"true", "false"}:
        raise_validation_exception(
            f"Error: Invalid value for '--skip_validation': '{skip_validation}' is not one of 'true', 'false'. "
        )
    if mode.lower() not in {"current", "experimental"}:
        raise_validation_exception(
            f"Error: Invalid value for '--mode': '{mode}' " f"is not one of 'current', 'experimental'. "
        )

    sdk_config = default_config.sdk_config if default_config.sdk_config else None
    catalog_name = catalog_name if catalog_name else default_config.catalog_name
    schema_name = schema_name if schema_name else default_config.schema_name

    config = MorphConfig(
        source=source.lower(),
        input_sql=input_sql,
        output_folder=output_folder,
        skip_validation=skip_validation.lower() == "true",  # convert to bool
        catalog_name=catalog_name,
        schema_name=schema_name,
        mode=mode,
        sdk_config=sdk_config,
    )

    status = morph(w, config)

    print(json.dumps(status))


@remorph.command
def reconcile(w: WorkspaceClient):
    """[EXPERIMENTAL] reconciles source to databricks datasets"""
    logger.info(f"user: {w.current_user.me()}")

    installation = Installation.assume_user_home(w, "remorph")
    _prompts = Prompts()

    reconcile_config = None
    try:
        logger.info("Loading ReconcileConfig `reconcile.yml` from Databricks Workspace...")
        reconcile_config = installation.load(ReconcileConfig)
    except NotFound as err:
        logger.warning(f"Cannot find previous `reconcile` installation: {err}")
    except (PermissionDenied, SerdeError, ValueError, AttributeError):
        logger.warning(f"Existing installation at {installation.install_folder()} is corrupted. Skipping...")

    reconfigure_msg = "Please use `remorph install` to re-configure ** reconcile ** module"
    # Re-configure `reconcile` module:
    # * when there is no `reconcile.yml` config on Databricks workspace OR
    # * when there is a `reconcile.yml` config and user wants to overwrite it
    if not reconcile_config:
        logger.error(f"`reconcile_config` not found / corrupted on Databricks Workspace.\n{reconfigure_msg}")
        return
    if _prompts.confirm(
        f"Would you like to overwrite workspace `reconcile_config` values:\n" f" {reconcile_config.__dict__}?"
    ):
        logger.info(reconfigure_msg)
        return

    catalog_or_schema = (
        reconcile_config.database_config.source_catalog
        if reconcile_config.database_config.source_catalog
        else reconcile_config.database_config.source_schema
    )

    # Creates the filename in the format of : `recon_config_<SOURCE>_<CATALOG_OR_SCHEMA>_<FILTER_TYPE>.json`
    # Ex: recon_config_snowflake_sample_data_all.json
    filename = f"recon_config_{reconcile_config.data_source}_{catalog_or_schema}_{reconcile_config.report_type}.json"

    try:
        logger.info(f"Loading TableRecon `{filename}` from Databricks Workspace...")
        table_recon = installation.load(type_ref=TableRecon, filename=filename)
    except NotFound as err:
        logger.error(f"Cannot find previous `reconcile` installation: {err}")
        raise err
    except (PermissionDenied, SerdeError, ValueError, AttributeError) as ex:
        logger.error(f"Existing installation at {installation.install_folder()}/{filename} is corrupted. Skipping...")
        raise ex

    assert table_recon, f"Error: Cannot load `recon_config` from {installation.install_folder()}/{filename}. "

    logger.info(f"Triggering the Job with job_id: `{reconcile_config.job_id}` ...")

    wait = w.jobs.run_now(job_id=reconcile_config.job_id)
    assert wait.run_id, (
        f"Error: Job {reconcile_config.job_id} execution failed." f" Please check the job logs for more details."
    )

    job_run_url = f"{w.config.host}/jobs/{reconcile_config.job_id}/runs/{wait.run_id}"
    if _prompts.confirm(f"Open Job Run URL `{job_run_url}` in the browser?"):
        webbrowser.open(job_run_url)
    logger.info(f"\nReconcile job started. Please check the job_url `{job_run_url}` for the current status.")


def _get_spark_session(ws: WorkspaceClient) -> SparkSession:
    return DatabricksSession.builder.sdkConfig(ws.config).getOrCreate()


@remorph.command
def generate_lineage(w: WorkspaceClient, source: str, input_sql: str, output_folder: str):
    """[Experimental] Generates a lineage of source SQL files or folder"""
    logger.info(f"User: {w.current_user.me()}")
    if source.lower() not in SQLGLOT_DIALECTS:
        raise_validation_exception(f"Error: Invalid value for '--source': '{source}' is not one of {DIALECTS}. ")
    if not os.path.exists(input_sql) or input_sql in {None, ""}:
        raise_validation_exception(f"Error: Invalid value for '--input_sql': Path '{input_sql}' does not exist.")
    if not os.path.exists(output_folder) or output_folder in {None, ""}:
        raise_validation_exception(
            f"Error: Invalid value for '--output-folder': Path '{output_folder}' does not exist."
        )

    lineage_generator(source, input_sql, output_folder)


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
