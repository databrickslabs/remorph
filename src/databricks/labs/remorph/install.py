import functools
import logging
import os
import time
import webbrowser
from datetime import timedelta
from functools import cached_property
from pathlib import Path

from databricks.labs.blueprint.entrypoint import get_logger, is_in_debug
from databricks.labs.blueprint.installation import Installation
from databricks.labs.blueprint.installer import InstallState
from databricks.labs.blueprint.parallel import ManyError, Threads
from databricks.labs.blueprint.tui import Prompts
from databricks.labs.blueprint.wheels import ProductInfo
from databricks.labs.remorph.__about__ import __version__
from databricks.labs.remorph.config import SQLGLOT_DIALECTS, MorphConfig
from databricks.labs.remorph.helpers import db_sql
from databricks.labs.remorph.helpers.deployment import TableDeployer
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import NotFound
from databricks.sdk.retries import retried
from databricks.sdk.service.sql import (
    CreateWarehouseRequestWarehouseType,
    EndpointInfoWarehouseType,
    SpotInstancePolicy,
)

logger = logging.getLogger(__name__)

PRODUCT_INFO = ProductInfo(__file__)
WAREHOUSE_PREFIX = "Remorph Transpiler Validation"


class WorkspaceInstaller:
    def __init__(self, ws: WorkspaceClient, prompts: Prompts = Prompts()):
        if "DATABRICKS_RUNTIME_VERSION" in os.environ:
            msg = "WorkspaceInstaller is not supposed to be executed in Databricks Runtime"
            raise SystemExit(msg)
        self._ws = ws
        self._prompts = prompts
        self._catalog_setup = CatalogSetup(ws)
        self._product_info = ProductInfo.from_class(MorphConfig)

    @cached_property
    def prompts(self) -> Prompts:
        return Prompts()

    @cached_property
    def _installation(self):
        try:
            return Installation.assume_user_home(self._ws, self._product_info.product_name())
        except RuntimeError:
            return Installation.assume_global(self._ws, self._product_info.product_name())

    def run(self):
        logger.info(f"Installing Remorph v{self._product_info.version()}")
        config = self.configure()
        workspace_installation = WorkspaceInstallation(
            config,
            self._installation,
            self._ws,
            self._prompts,
            verify_timeout=timedelta(minutes=2),
            product_info=self._product_info,
        )
        try:
            workspace_installation.run()
        except ManyError as err:
            if len(err.errs) == 1:
                raise err.errs[0] from None
            raise err
        return config

    def configure(self) -> MorphConfig:
        try:
            return self._installation.load(MorphConfig)
        except NotFound as err:
            logger.debug(f"Cannot find previous installation: {err}")
        return self._configure_new_installation()

    def _prompt_for_new_installation(self) -> MorphConfig:
        logger.info("Please answer a couple of questions to configure Remorph")

        # default params
        catalog_name = "transpiler_test"
        schema_name = "convertor_test"
        ws_config = None

        source_prompt = self._prompts.choice("Select the source", SQLGLOT_DIALECTS.keys())
        source = source_prompt.lower()

        skip_validation = self._prompts.confirm("Do you want to Skip Validation")

        if not skip_validation:
            ws_config = self._configure_runtime()
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

        return MorphConfig(
            source=source,
            skip_validation=skip_validation,
            catalog_name=catalog_name,
            schema_name=schema_name,
            sdk_config=ws_config,
            mode="current",  # mode will not have a prompt as this is hidden flag
        )

    def _configure_new_installation(self) -> MorphConfig:
        config = self._prompt_for_new_installation()

        self._installation.save(config)
        ws_file_url = self._installation.workspace_link(config.__file__)
        if self._prompts.confirm(f"Open config file in the browser and continue installing {ws_file_url}?"):
            webbrowser.open(ws_file_url)
        return config

    def _configure_runtime(self) -> dict[str, str]:
        if self._prompts.confirm("Do you want to use SQL Warehouse for validation?"):
            warehouse_id = self._configure_warehouse()
            return {"warehouse_id": warehouse_id}

        if self._ws.config.cluster_id:
            logger.info(f"Using cluster {self._ws.config.cluster_id} for validation")
            return {"cluster_id": self._ws.config.cluster_id}

        cluster_id = self._prompts.question("Enter a valid cluster_id to proceed")
        return {"cluster_id": cluster_id}

    def _configure_warehouse(self):
        def warehouse_type(_):
            return _.warehouse_type.value if not _.enable_serverless_compute else "SERVERLESS"

        pro_warehouses = {"[Create new PRO SQL warehouse]": "create_new"} | {
            f"{_.name} ({_.id}, {warehouse_type(_)}, {_.state.value})": _.id
            for _ in self._ws.warehouses.list()
            if _.warehouse_type == EndpointInfoWarehouseType.PRO
        }
        warehouse_id = self._prompts.choice_from_dict(
            "Select PRO or SERVERLESS SQL warehouse to run validation on", pro_warehouses
        )
        if warehouse_id == "create_new":
            new_warehouse = self._ws.warehouses.create(
                name=f"{WAREHOUSE_PREFIX} {time.time_ns()}",
                spot_instance_policy=SpotInstancePolicy.COST_OPTIMIZED,
                warehouse_type=CreateWarehouseRequestWarehouseType.PRO,
                cluster_size="Small",
                max_num_clusters=1,
            )
            warehouse_id = new_warehouse.id
        return warehouse_id

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
        logger.info(f"Installing Remorph v{PRODUCT_INFO.version()}")
        install_tasks = [self._configure_recon_metadata]
        Threads.strict("installing components", install_tasks)
        self._installation.save(self._config)
        logger.info("Installation completed successfully! Please refer to the documentation for the next steps.")

    def _configure_recon_metadata(self):
        setup = ReconMetadataSetup(self._ws, self._product_info.product_name())
        setup.run()


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


class ReconMetadataSetup:

    def __init__(self, ws: WorkspaceClient, product_name: str):
        self._ws = ws
        self._product_name = product_name
        self._catalog_setup = CatalogSetup(ws)
        self._recon_catalog_name = f"{product_name}"
        self._recon_schema_name = "reconcile"

    def configure_catalog(self):
        try:
            return self._catalog_setup.get(self._recon_catalog_name)
        except NotFound:
            self._catalog_setup.create(self._recon_catalog_name)
        return self._recon_catalog_name

    def configure_schema(self):
        try:
            return self._catalog_setup.get_schema(f"{self._recon_catalog_name}.{self._recon_schema_name}")
        except NotFound:
            logger.info(f" Creating new Schema {self._recon_catalog_name}.{self._recon_schema_name}")
            self._catalog_setup.create_schema(self._recon_schema_name, self._recon_catalog_name)
        return self._recon_schema_name

    def deploy_tables(self):

        config = MorphConfig(
            source=self._product_name, catalog_name=self._recon_catalog_name, schema_name=self._recon_schema_name
        )
        sql_backend = db_sql.get_sql_backend(self._ws, config)
        deployer = TableDeployer(sql_backend, config)

        table = functools.partial(deployer.deploy_table)
        Threads.strict(
            "deploy tables",
            [
                functools.partial(table, "main", "queries/tables/reconcile/main.sql"),
                functools.partial(table, "metrics", "queries/tables/reconcile/metrics.sql"),
                functools.partial(table, "details", "queries/tables/reconcile/details.sql"),
            ],
        )

    def run(self):
        self.configure_catalog()
        self.configure_schema()
        self.deploy_tables()


if __name__ == "__main__":
    logger = get_logger(__file__)
    logger.setLevel("INFO")
    if is_in_debug():
        logging.getLogger('databricks').setLevel(logging.DEBUG)

    # current = Installation(workspace_client, PRODUCT_INFO.product_name())
    workspace_installer = WorkspaceInstaller(WorkspaceClient(product="remorph", product_version=__version__))
    workspace_installer.run()
