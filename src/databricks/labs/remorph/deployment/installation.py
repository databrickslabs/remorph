import logging

from databricks.labs.blueprint.installation import Installation
from databricks.labs.blueprint.tui import Prompts
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import NotFound

from databricks.labs.remorph.config import RemorphConfigs
from databricks.labs.remorph.deployment.recon import ReconDeployment

logger = logging.getLogger("databricks.labs.remorph.install")


class WorkspaceInstallation:
    def __init__(
        self,
        ws: WorkspaceClient,
        prompts: Prompts,
        installation: Installation,
        recon_deployment: ReconDeployment,
    ):
        self._ws = ws
        self._prompts = prompts
        self._installation = installation
        self._recon_deployment = recon_deployment

    def install(self, config: RemorphConfigs):
        if config.reconcile:
            self._recon_deployment.install(config.reconcile)

    def uninstall(self, config: RemorphConfigs):
        # This will remove all the Remorph modules
        if not self._prompts.confirm(
            "Do you want to uninstall Remorph from the workspace too, this would "
            "remove Remorph project folder, jobs, metadata and dashboards"
        ):
            return
        logger.info(f"Uninstalling Remorph from {self._ws.config.host}.")
        try:
            self._installation.files()
        except NotFound:
            logger.error(f"Check if {self._installation.install_folder()} is present. Aborting uninstallation.")
            return

        if config.morph:
            logging.info(
                f"Won't remove transpile validation schema `{config.morph.schema_name}` "
                f"from catalog `{config.morph.catalog_name}`. Please remove it manually."
            )

        if config.reconcile:
            self._recon_deployment.uninstall(config.reconcile)

        self._installation.remove()
        logger.info("Uninstallation completed successfully.")
