import logging
import webbrowser

from databricks.labs.blueprint.installation import Installation, SerdeError
from databricks.labs.blueprint.tui import Prompts
from databricks.labs.remorph.config import ReconcileConfig, TableRecon
from databricks.sdk.errors import NotFound, PermissionDenied
from databricks.sdk import WorkspaceClient

logger = logging.getLogger(__name__)

README_RECON_REPO = "https://github.com/databrickslabs/remorph/blob/main/docs/README_RECON.md"


class ReconcileUtils:
    def __init__(self, w: WorkspaceClient, installation: Installation, prompts: Prompts = Prompts()):
        self._ws = w
        self._installation = installation
        self._prompts = prompts

    def _load_configs(self) -> tuple[ReconcileConfig, TableRecon] | None:
        reconcile_config = None
        try:
            logger.info("Loading ReconcileConfig `reconcile.yml` from Databricks Workspace...")
            reconcile_config = self._installation.load(ReconcileConfig)
        except NotFound as err:
            logger.warning(f"Cannot find previous `reconcile` installation: {err}")
        except (PermissionDenied, SerdeError, ValueError, AttributeError):
            logger.warning(f"Existing installation at {self._installation.install_folder()} is corrupted. Skipping...")

        reconfigure_msg = "Please use `remorph install` to re-configure ** reconcile ** module"
        # Re-configure `reconcile` module:
        # * when there is no `reconcile.yml` config on Databricks workspace OR
        # * when there is a `reconcile.yml` config and user wants to overwrite it
        if not reconcile_config:
            logger.error(f"`reconcile_config` not found / corrupted on Databricks Workspace.\n{reconfigure_msg}")
            return None
        if self._prompts.confirm(
            f"Would you like to overwrite workspace `reconcile_config` values:\n" f" {reconcile_config.__dict__}?"
        ):
            logger.info(reconfigure_msg)
            return None

        catalog_or_schema = (
            reconcile_config.database_config.source_catalog
            if reconcile_config.database_config.source_catalog
            else reconcile_config.database_config.source_schema
        )

        # Creates the filename in the format of : `recon_config_<SOURCE>_<CATALOG_OR_SCHEMA>_<FILTER_TYPE>.json`
        # Ex: recon_config_snowflake_sample_data_all.json
        filename = (
            f"recon_config_{reconcile_config.data_source}_{catalog_or_schema}_" f"{reconcile_config.report_type}.json"
        )

        try:
            logger.info(f"Loading TableRecon `{filename}` from Databricks Workspace...")
            table_recon = self._installation.load(type_ref=TableRecon, filename=filename)
        except NotFound as err:
            logger.error(
                f"Cannot find recon_config file : {err}. \nPlease refer this "
                f"{README_RECON_REPO} to create the recon_config file."
            )
            return None
        except (PermissionDenied, SerdeError, ValueError, AttributeError) as ex:
            logger.error(
                f"Existing recon_config file at `{self._installation.install_folder()}/{filename}` is corrupted. `{ex}`"
                f"\nPlease validate the file, verify it using {README_RECON_REPO}"
            )
            return None

        assert table_recon, f"Error: Cannot load `recon_config` from {self._installation.install_folder()}/{filename}. "

        return reconcile_config, table_recon

    def run(self):

        reconcile_config = None
        table_recon = None

        if self._load_configs():
            reconcile_config, table_recon = self._load_configs()

        assert reconcile_config, "Error: Cannot load `reconcile_config`"
        assert table_recon, "Error: Cannot load `recon_config`"

        logger.info(f"Triggering the Job with job_id: `{reconcile_config.job_id}` ...")

        wait = self._ws.jobs.run_now(job_id=reconcile_config.job_id)
        assert wait.run_id, (
            f"Error: Job {reconcile_config.job_id} execution failed." f" Please check the job logs for more details."
        )

        job_run_url = f"{self._ws.config.host}/jobs/{reconcile_config.job_id}/runs/{wait.run_id}"
        if self._prompts.confirm(f"Open Job Run URL `{job_run_url}` in the browser?"):
            webbrowser.open(job_run_url)
        logger.info(f"\nReconcile job started. Please check the job_url `{job_run_url}` for the current status.")

        return True
