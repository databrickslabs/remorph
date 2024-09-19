import logging

from databricks.labs.blueprint.installation import Installation
from databricks.labs.blueprint.tui import Prompts
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import NotFound

from databricks.labs.remorph.config import RemorphConfigs
from databricks.labs.remorph.deployment.recon import ReconDeployment
from databricks.labs.blueprint.wheels import WheelsV2

from databricks.sdk.errors.platform import InvalidParameterValue
from databricks.labs.blueprint.upgrades import Upgrades


logger = logging.getLogger("databricks.labs.remorph.install")


class WorkspaceInstallation:
    def __init__(
        self,
        ws: WorkspaceClient,
        prompts: Prompts,
        installation: Installation,
        recon_deployment: ReconDeployment,
        wheels: WheelsV2,
        upgrades: Upgrades,
    ):
        self._ws = ws
        self._prompts = prompts
        self._installation = installation
        self._recon_deployment = recon_deployment
        self._wheels = wheels
        self._upgrades = upgrades

    def _apply_upgrades(self):
        try:
            self._upgrades.apply(self._ws)
        except (InvalidParameterValue, NotFound) as err:
            logger.warning(f"Unable to apply Upgrades due to: {err}")

    def _upload_wheel(self):
        with self._wheels:
            wheel_paths = [self._wheels.upload_to_wsfs()]
            wheel_paths = [f"/Workspace{wheel}" for wheel in wheel_paths]
            return wheel_paths

    def install(self, config: RemorphConfigs):
        wheel_paths: list[str] = self._upload_wheel()
        if config.reconcile:
            self._recon_deployment.install(config.reconcile, wheel_paths)
        self._apply_upgrades()

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
