import logging
from datetime import timedelta

from databricks.labs.blueprint.installation import Installation
from databricks.labs.blueprint.tui import Prompts
from databricks.labs.blueprint.wheels import ProductInfo
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import NotFound

from databricks.labs.remorph.__about__ import __version__
from databricks.labs.remorph.config import MorphConfig

logger = logging.getLogger("databricks.labs.remorph.install")

PRODUCT_INFO = ProductInfo(__file__)


class WorkspaceUnInstallation:
    def __init__(
        self,
        config: MorphConfig,
        installation: Installation,
        w: WorkspaceClient,
        prompts: Prompts,
        verify_timeout: timedelta,
    ):
        self._config = config
        self._installation = installation
        self._ws = w
        self._prompts = prompts
        self._verify_timeout = verify_timeout

    def uninstall(self):
        if self._prompts and not self._prompts.confirm(
            "Do you want to uninstall remorph from the workspace too, this would remove remorph project folder"
        ):
            return
        # TODO: this is incorrect, fetch the remote version (that appeared only in Feb 2024)
        logger.info(f"Deleting Remorph v{PRODUCT_INFO.version()} from {self._ws.config.host}")
        try:
            self._installation.files()
        except NotFound:
            logger.error(f"Check if {self._installation.install_folder()} is present")
            return
        self._installation.remove()
        logger.info("UnInstalling Remorph complete")


if __name__ == "__main__":
    logger.setLevel("INFO")
    ws = WorkspaceClient(product="remorph", product_version=__version__)
    current = Installation(ws, PRODUCT_INFO.product_name())
    morph_config = current.load(MorphConfig)

    uninstaller = WorkspaceUnInstallation(morph_config, current, ws, Prompts(), timedelta(minutes=2))
    uninstaller.uninstall()
