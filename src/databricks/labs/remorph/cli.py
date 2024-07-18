import os

from pyspark.sql import SparkSession

from databricks.connect import DatabricksSession
from databricks.labs.blueprint.cli import App
from databricks.labs.blueprint.entrypoint import get_logger
from databricks.labs.blueprint.installation import Installation
from databricks.labs.remorph.config import SQLGLOT_DIALECTS, DIALECTS
from databricks.labs.remorph.helpers.recon_config_utils import ReconConfigPrompts
from databricks.labs.remorph.helpers.reconcile_utils import ReconcileUtils
from databricks.labs.remorph.helpers.transpile_utils import TranspileUtils, raise_validation_exception
from databricks.labs.remorph.lineage import lineage_generator
from databricks.sdk import WorkspaceClient

remorph = App(__file__)
logger = get_logger(__file__)


@remorph.command
def transpile(w: WorkspaceClient):
    """[EXPERIMENTAL] reconciles source to databricks datasets"""
    logger.info(f"user: {w.current_user.me()}")

    installation = Installation.assume_user_home(w, "remorph")

    utils = TranspileUtils(w, installation)
    utils.run()


@remorph.command
def reconcile(w: WorkspaceClient):
    """[EXPERIMENTAL] reconciles source to databricks datasets"""
    logger.info(f"user: {w.current_user.me()}")

    installation = Installation.assume_user_home(w, "remorph")

    utils = ReconcileUtils(w, installation)
    utils.run()


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
