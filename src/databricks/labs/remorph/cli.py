# pylint: disable=(wrong-import-order,ungrouped-imports,useless-suppression)
import json
import os

from databricks.labs.blueprint.cli import App
from databricks.labs.blueprint.entrypoint import get_logger
from databricks.sdk import WorkspaceClient

from databricks.labs.remorph.config import MorphConfig
from databricks.labs.remorph.helpers.recon_config_utils import (
    ReconConfigPrompts,
    recon_source_choices,
)
from databricks.labs.remorph.reconcile.execute import recon
from databricks.labs.remorph.transpiler.execute import morph

remorph = App(__file__)
logger = get_logger(__file__)


def raise_validation_exception(msg: str) -> Exception:
    raise ValueError(msg)


@remorph.command
def transpile(
    w: WorkspaceClient,
    source: str,
    input_sql: str,
    output_folder: str,
    skip_validation: str,
    catalog_name: str,
    schema_name: str,
):
    """transpiles source dialect to databricks dialect"""
    logger.info(f"user: {w.current_user.me()}")

    if source.lower() not in {"snowflake", "tsql"}:
        raise_validation_exception(
            f"Error: Invalid value for '--source': '{source}' is not one of 'snowflake', 'tsql'. "
        )
    if not os.path.exists(input_sql) or input_sql in {None, ""}:
        raise_validation_exception(f"Error: Invalid value for '--input_sql': Path '{input_sql}' does not exist.")
    if output_folder == "":
        output_folder = None
    if skip_validation.lower() not in {"true", "false"}:
        raise_validation_exception(
            f"Error: Invalid value for '--skip_validation': '{skip_validation}' is not one of 'true', 'false'. "
        )

    config = MorphConfig(
        source=source.lower(),
        input_sql=input_sql,
        output_folder=output_folder,
        skip_validation=skip_validation.lower() == "true",  # convert to bool
        catalog_name=catalog_name,
        schema_name=schema_name,
        sdk_config=w.config,
    )

    status = morph(w, config)

    print(json.dumps(status))


@remorph.command
def reconcile(w: WorkspaceClient, recon_conf: str, conn_profile: str, source: str, report: str):
    """reconciles source to databricks datasets"""
    logger.info(f"user: {w.current_user.me()}")
    if not os.path.exists(recon_conf) or recon_conf in {None, ""}:
        raise_validation_exception(f"Error: Invalid value for '--recon_conf': Path '{recon_conf}' does not exist.")
    if not os.path.exists(conn_profile) or conn_profile in {None, ""}:
        raise_validation_exception(f"Error: Invalid value for '--conn_profile': Path '{conn_profile}' does not exist.")
    if source.lower() not in "snowflake":
        raise_validation_exception(f"Error: Invalid value for '--source': '{source}' is not one of 'snowflake'. ")
    if report.lower() not in {"data", "schema", "all"}:
        raise_validation_exception(
            f"Error: Invalid value for '--report': '{report}' is not one of 'data', 'schema', 'all' "
        )

    recon(recon_conf, conn_profile, source, report)


@remorph.command
def generate_recon_config(w: WorkspaceClient):
    """generates config file for reconciliation"""
    logger.info("Generating config file for reconcile")
    recon_conf = ReconConfigPrompts(w)

    # Prompt for source
    source = recon_conf.prompts.choice("Select the source", recon_source_choices)

    # Check for Secrets Scope
    if not recon_conf.prompts.confirm(f"Have you setup the secrets for the `{source}` connection?"):
        raise_validation_exception(
            f"Error: Secrets are needed for `{source}` reconciliation."
            f"\nUse `remorph setup-recon-secrets` to setup Scope and Secrets."
        )
    recon_config = recon_conf.prompt_config_details(source)
    print(json.dumps(recon_config.__dict__))
    # recon_conf.save_config_details(recon_config)


@remorph.command
def validate_recon_config(w: WorkspaceClient):
    """validates reconciliation config file"""
    logger.info("Validating reconcile config file")
    print(w.catalogs.list())


@remorph.command
def setup_recon_secrets(w: WorkspaceClient):
    """Setup reconciliation connection profile details as Secrets in Databricks Workspace"""
    recon_conf = ReconConfigPrompts(w)

    # Prompt for source
    source = recon_conf.prompts.choice("Select the source", recon_source_choices)

    logger.info(f"Setting up Scope, Secrets for `{source}` reconciliation")
    recon_conf.prompt_connection_details(source)


if __name__ == "__main__":
    remorph()
