import logging
import os
import webbrowser
from datetime import timedelta
from functools import cached_property
from pathlib import Path

from databricks.labs.blueprint.entrypoint import get_logger, is_in_debug
from databricks.labs.blueprint.installation import Installation
from databricks.labs.blueprint.installer import InstallState
from databricks.labs.blueprint.tui import Prompts
from databricks.labs.blueprint.wheels import ProductInfo
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import NotFound

from databricks.labs.remorph.__about__ import __version__
from databricks.labs.remorph.config import MorphConfig, ReconcileConfig
from databricks.labs.remorph.helpers.install_utils import CatalogSetup, InstallPrompts

logger = logging.getLogger(__name__)

PRODUCT_INFO = ProductInfo(__file__)


class WorkspaceInstaller:
    def __init__(self, ws: WorkspaceClient, prompts: Prompts = Prompts()):
        if "DATABRICKS_RUNTIME_VERSION" in os.environ:
            msg = "WorkspaceInstaller is not supposed to be executed in Databricks Runtime"
            raise SystemExit(msg)
        self._ws = ws
        self._prompts = prompts
        self._catalog_setup = CatalogSetup(ws)
        self._product_info = ProductInfo.from_class(MorphConfig)
        self._install = InstallPrompts(ws, prompts)

    @cached_property
    def _installation(self):
        try:
            # Installation.assume_user_home(self._ws, self._product_info.product_name())
            folder_path = f"/Users/{self._ws.current_user.me().user_name}/.remorph_demo"
            return Installation(self._ws, self._product_info.product_name(), install_folder=folder_path)
        except RuntimeError:
            return Installation.assume_global(self._ws, self._product_info.product_name())

    def run(self):
        logger.info(f"Installing Remorph v{self._product_info.version()}")
        config = self.configure()
        # workspace_installation = WorkspaceInstallation(
        #     config,
        #     self._installation,
        #     self._ws,
        #     self._prompts,
        #     verify_timeout=timedelta(minutes=2),
        #     product_info=self._product_info,
        # )
        # try:
        #     workspace_installation.run()
        # except ManyError as err:
        #     if len(err.errs) == 1:
        #         raise err.errs[0] from None
        #     raise err
        logger.info("Installation completed successfully! Please refer to the documentation for the next steps.")
        return config

    def configure(self) -> tuple[MorphConfig | None, ReconcileConfig | None]:
        """
        Returns the MorphConfig If it exists on the Databricks Workspace,
         else prompts for the new Installation
        :return:
        """
        morph_config = None
        reconcile_config = None

        try:
            morph_config = self._installation.load(MorphConfig)
        except NotFound as err:
            logger.debug(f"Cannot find previous `transpile` installation: {err}")

        try:
            reconcile_config = self._installation.load(ReconcileConfig)
        except NotFound as err:
            logger.debug(f"Cannot find previous `reconcile` installation: {err}")

        if morph_config or reconcile_config:
            return morph_config, reconcile_config

        return self._configure_new_installation()

    def _save_and_open_config(self, module: str, config: MorphConfig | ReconcileConfig):
        logger.info(f"Saving the ** {module} ** configuration in Databricks Workspace")
        self._installation.save(config)
        ws_file_url = self._installation.workspace_link(config.__file__)
        if self._prompts.confirm(f"Open `{config.__file__}` in the browser and continue installing?"):
            webbrowser.open(ws_file_url)

    def _configure_new_installation(self) -> tuple[MorphConfig | None, ReconcileConfig | None]:
        """
        Prompts for the new Installation and saves the configuration
        :return: MorphConfig
        """
        morph_config, reconcile_config = self._install.prompt_for_new_installation()
        if morph_config:
            self._save_and_open_config("transpile", morph_config)
        if reconcile_config:
            self._save_and_open_config("reconcile", reconcile_config)

        return morph_config, reconcile_config


class WorkspaceInstallation:
    def __init__(
        self,
        config: MorphConfig,
        installation: Installation,
        ws: WorkspaceClient,
        prompts: Prompts,
        verify_timeout: timedelta,
        product_info: ProductInfo,
    ):
        self._config = config
        self._installation = installation
        self._ws = ws
        self._prompts = prompts
        self._verify_timeout = verify_timeout
        self._state = InstallState.from_installation(installation)
        self._this_file = Path(__file__)
        self._product_info = product_info

    def run(self):
        logger.info(f"Installing Remorph v{self._product_info.version()}")
        self._installation.save(self._config)
        logger.info("Installation completed successfully! Please refer to the documentation for the next steps.")


if __name__ == "__main__":
    logger = get_logger(__file__)
    logger.setLevel("INFO")
    if is_in_debug():
        logging.getLogger('databricks').setLevel(logging.DEBUG)

    installer = WorkspaceInstaller(WorkspaceClient(product="remorph", product_version=__version__))
    installer.run()
