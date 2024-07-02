import logging

from databricks.sdk.errors import NotFound

from databricks.labs.remorph.config import RemorphConfigs
from databricks.labs.remorph.contexts.application import CliContext
from databricks.labs.remorph.deployment.recon import ReconDeployment

logger = logging.getLogger("databricks.labs.remorph.install")


class WorkspaceInstallation:
    def __init__(
        self,
        context: CliContext,
        recon_deployment: ReconDeployment,
    ):
        self._context = context
        self._recon_deployment = recon_deployment

    def install(self, config: RemorphConfigs):
        if config.reconcile:
            self._recon_deployment.install(config.reconcile)

    def uninstall(self):
        # This will remove all the Remorph modules
        if not self._context.prompts.confirm(
            "Do you want to uninstall Remorph from the workspace too, this would "
            "remove Remorph project folder, jobs, metadata and dashboards"
        ):
            return
        logger.info(f"Uninstalling Remorph from {self._context.workspace_client.config.host}.")
        try:
            self._context.installation.files()
        except NotFound:
            logger.error(f"Check if {self._context.installation.install_folder()} is present. Aborting uninstallation.")
            return

        if self._context.transpile_config:
            logging.info(
                f"Won't remove transpile validation schema `{self._context.transpile_config.schema_name}` "
                f"from catalog `{self._context.transpile_config.catalog_name}`. Please remove it manually."
            )

        if self._context.recon_config:
            self._recon_deployment.uninstall(self._context.recon_config)

        self._context.installation.remove()
        logger.info("Uninstallation completed successfully.")
