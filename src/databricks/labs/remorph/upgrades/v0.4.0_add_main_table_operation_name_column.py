# pylint: disable=invalid-name,unused-argument
import logging

from databricks.labs.blueprint.installation import Installation
from databricks.sdk import WorkspaceClient

from databricks.labs.remorph.config import ReconcileConfig
from databricks.labs.remorph.contexts.application import ApplicationContext
from databricks.labs.remorph.deployment.recon import RECON_JOB_NAME
from databricks.labs.remorph.helpers import db_sql

logger = logging.getLogger(__name__)


def _upgrade_reconcile_metadata_main_table(installation: Installation, ws: WorkspaceClient):
    reconcile_config = installation.load(ReconcileConfig)
    table_identifier = f"{reconcile_config.metadata_config.catalog}.{reconcile_config.metadata_config.schema}.main"
    sql = f"ALTER TABLE {table_identifier} ADD COLUMN operation_name  STRING AFTER report_type"
    db_sql.get_sql_backend(ws).execute(sql)
    installation.save(reconcile_config)


def _upgrade_reconcile_workflow(installation, ws):
    context = ApplicationContext(ws)
    context.job_deployment.deploy_recon_job(RECON_JOB_NAME, context.recon_config)


def upgrade(installation: Installation, ws: WorkspaceClient):
    _upgrade_reconcile_metadata_main_table(installation, ws)
    _upgrade_reconcile_workflow(installation, ws)
