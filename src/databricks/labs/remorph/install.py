import logging
import os
import webbrowser
from datetime import timedelta
from pathlib import Path

from databricks.labs.blueprint.entrypoint import get_logger
from databricks.labs.blueprint.installation import Installation
from databricks.labs.blueprint.installer import InstallState
from databricks.labs.blueprint.tui import Prompts
from databricks.labs.blueprint.wheels import ProductInfo
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import NotFound
from databricks.sdk.retries import retried

from databricks.labs.remorph.__about__ import __version__
from databricks.labs.remorph.config import MorphConfig

logger = logging.getLogger(__name__)

PRODUCT_INFO = ProductInfo(__file__)


class WorkspaceInstaller:
    def __init__(self, prompts: Prompts, installation: Installation, ws: WorkspaceClient):
        if "DATABRICKS_RUNTIME_VERSION" in os.environ:
            msg = "WorkspaceInstaller is not supposed to be executed in Databricks Runtime"
            raise SystemExit(msg)
        self._ws = ws
        self._installation = installation
        self._prompts = prompts
        self._catalog_setup = CatalogSetup(ws)

    def run(self):
        logger.info(f"Installing Remorph v{PRODUCT_INFO.version()}")
        config = self.configure()
        workspace_installation = WorkspaceInstallation(
            config,
            self._installation,
            self._ws,
            self._prompts,
            verify_timeout=timedelta(minutes=2),
        )
        workspace_installation.run()

    def configure(self) -> MorphConfig:
        try:
            return self._installation.load(MorphConfig)
        except NotFound as err:
            logger.debug(f"Cannot find previous installation: {err}")
        logger.info("Please answer a couple of questions to configure Remorph")

        source_prompt = self._prompts.choice("Select the source", ["snowflake", "tsql"])
        source = source_prompt.lower()

        skip_validation = self._prompts.confirm("Do you want to Skip Validation")

        catalog_name = self._prompts.question("Enter catalog_name")

        try:
            self._catalog_setup.get(catalog_name)
        except NotFound:
            self.setup_catalog(catalog_name)

        schema_name = self._prompts.question("Enter schema_name")

        try:
            self._catalog_setup.get_schema(f"{catalog_name}.{schema_name}")
        except NotFound:
            self.setup_schema(catalog_name, schema_name)

        config = MorphConfig(
            source=source,
            skip_validation=skip_validation,
            catalog_name=catalog_name,
            schema_name=schema_name,
            sdk_config=None,
        )

        ws_file_url = self._installation.save(config)
        if self._prompts.confirm("Open config file in the browser and continue installing?"):
            webbrowser.open(ws_file_url)
        return config

    @retried(on=[NotFound], timeout=timedelta(minutes=5))
    def setup_catalog(self, catalog_name: str):
        allow_catalog_creation = self._prompts.confirm(
            f"""Catalog {catalog_name} not found.\
                    \nDo you want to create a new one?"""
        )
        if not allow_catalog_creation:
            msg = "Catalog is needed to setup Remorph"
            raise SystemExit(msg)

        logger.info(f" Creating new Catalog {catalog_name}")
        self._catalog_setup.create(catalog_name)

    @retried(on=[NotFound], timeout=timedelta(minutes=5))
    def setup_schema(self, catalog_name: str, schema_name: str):
        allow_schema_creation = self._prompts.confirm(
            f"""Schema {schema_name} not found in Catalog {catalog_name}\
                    \nDo you want to create a new Schema?"""
        )
        if not allow_schema_creation:
            msg = "Schema is needed to setup Remorph"
            raise SystemExit(msg)

        logger.info(f" Creating new Schema {catalog_name}.{schema_name}")
        self._catalog_setup.create_schema(schema_name, catalog_name)


class WorkspaceInstallation:
    def __init__(
        self,
        config: MorphConfig,
        installation: Installation,
        ws: WorkspaceClient,
        prompts: Prompts,
        verify_timeout: timedelta,
    ):
        self._config = config
        self._installation = installation
        self._ws = ws
        self._prompts = prompts
        self._verify_timeout = verify_timeout
        self._state = InstallState.from_installation(installation)
        self._this_file = Path(__file__)

    def run(self):
        logger.info(f"Installing Remorph v{PRODUCT_INFO.version()}")
        self._installation.save(self._config)
        logger.info("Installation completed successfully! Please refer to the documentation for the next steps.")


class CatalogSetup:
    def __init__(self, ws: WorkspaceClient):
        self._ws = ws

    def create(self, name: str):
        logger.debug(f"Creating Catalog {name}")
        catalog_info = self._ws.catalogs.create(name, comment="Created as part of Remorph setup")
        logger.info(f"Catalog {name} created")
        return catalog_info

    def get(self, name: str):
        try:
            logger.debug(f"Searching for Catalog {name}")
            catalog_info = self._ws.catalogs.get(name)
            logger.info(f"Catalog {name} found")
            return catalog_info.name
        except NotFound as err:
            logger.error(f"Cannot find Catalog: {err}")
            raise err

    def create_schema(self, name: str, catalog_name: str):
        logger.debug(f"Creating Schema {name} in Catalog {catalog_name}")
        schema_info = self._ws.schemas.create(name, catalog_name, comment="Created as part of Remorph setup")
        logger.info(f"Created Schema {name} in Catalog {catalog_name}")
        return schema_info

    def get_schema(self, name: str):
        try:
            logger.debug(f"Searching for Schema {name}")
            schema_info = self._ws.schemas.get(name)
            logger.info(f"Schema {name} found")
            return schema_info.name
        except NotFound as err:
            logger.error(f"Cannot find Schema: {err}")
            raise err


if __name__ == "__main__":
    logger = get_logger(__file__)
    logger.setLevel("INFO")

    workspace_client = WorkspaceClient(product="remorph", product_version=__version__)
    current = Installation(workspace_client, PRODUCT_INFO.product_name())
    installer = WorkspaceInstaller(Prompts(), current, workspace_client)
    installer.run()
