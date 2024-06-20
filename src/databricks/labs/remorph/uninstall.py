import logging
from datetime import timedelta
from ast import literal_eval

from databricks.labs.blueprint.installation import Installation
from databricks.labs.blueprint.tui import Prompts
from databricks.labs.blueprint.wheels import ProductInfo
from databricks.labs.remorph.__about__ import __version__
from databricks.labs.remorph.config import MorphConfig, ReconcileConfig, RemorphConfigs
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import NotFound
from databricks.sdk.errors.platform import PermissionDenied
from databricks.labs.blueprint.installation import SerdeError

logger = logging.getLogger("databricks.labs.remorph.install")

PRODUCT_INFO = ProductInfo(__file__)


class WorkspaceUnInstaller:
    def __init__(
        self,
        installation: Installation,
        w: WorkspaceClient,
        prompts: Prompts,
        verify_timeout: timedelta,
    ):
        self._installation = installation
        self._ws = w
        self._prompts = prompts
        self._verify_timeout = verify_timeout

    def _load_configs(self) -> RemorphConfigs:
        morph_config = None
        reconcile_config = None
        try:
            morph_config = self._installation.load(MorphConfig)
        except NotFound as err:
            logger.warning(f"Cannot find previous `transpile` installation: {err}")
        except (PermissionDenied, SerdeError, ValueError, AttributeError):
            logger.warning(f"Existing installation at {self._installation.install_folder()} is corrupted.")

        try:
            reconcile_config = self._installation.load(ReconcileConfig)
        except NotFound as err:
            logger.warning(f"Cannot find previous `reconcile` installation: {err}")
        except (PermissionDenied, SerdeError, ValueError, AttributeError):
            logger.warning(f"Existing installation at {self._installation.install_folder()} is corrupted.")

        return RemorphConfigs(morph_config, reconcile_config)

    def uninstall(self) -> bool:
        logger.info("UnInstalling ** remorph ** started...")
        ws_uninstaller = WorkspaceUnInstallation(
            self._load_configs(), self._installation, self._ws, self._prompts, self._verify_timeout
        )
        return ws_uninstaller.uninstall()


class WorkspaceUnInstallation:
    def __init__(
        self,
        remorph_configs: RemorphConfigs,
        installation: Installation,
        w: WorkspaceClient,
        prompts: Prompts,
        verify_timeout: timedelta,
    ):
        self._configs = remorph_configs
        self._installation = installation
        self._ws = w
        self._prompts = prompts
        self._verify_timeout = verify_timeout

    def _delete_workflow(self):
        if self._configs.reconcile and self._configs.reconcile.job_id:
            self._ws.jobs.delete(literal_eval(self._configs.reconcile.job_id))
            logger.info(f"Deleted Reconcile Workflow with id: `{self._configs.reconcile.job_id}`")
            return True
        return False

    def uninstall(self):
        if self._prompts and not self._prompts.confirm(
            "Do you want to uninstall ** remorph ** from the workspace too,"
            " this would remove `remorph` project folder"
        ):
            return False
        # TODO: this is incorrect, fetch the remote version (that appeared only in Feb 2024)
        logger.info(f"Deleting `remorph v{PRODUCT_INFO.version()}` from {self._ws.config.host}...")
        try:
            self._installation.files()
        except NotFound:
            logger.error(f"Check if {self._installation.install_folder()} is present")
            return False
        self._delete_workflow()
        self._installation.remove()

        logger.info("UnInstalling ** remorph ** completed...")
        return True


if __name__ == "__main__":
    logger.setLevel("INFO")
    ws = WorkspaceClient(product="remorph", product_version=__version__)
    current = Installation(ws, PRODUCT_INFO.product_name())

    uninstaller = WorkspaceUnInstaller(current, ws, Prompts(), timedelta(minutes=2))
    uninstaller.uninstall()
