import logging
import os
import time
import webbrowser
from datetime import timedelta
from importlib.resources import files, as_file
from pathlib import Path

from databricks.labs.blueprint.entrypoint import get_logger, is_in_debug
from databricks.labs.blueprint.installation import Installation, SerdeError
from databricks.labs.blueprint.installer import InstallState
from databricks.labs.blueprint.parallel import ManyError
from databricks.labs.blueprint.tui import Prompts
from databricks.labs.blueprint.wheels import ProductInfo
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import NotFound
from databricks.sdk.errors import PermissionDenied
from databricks.sdk.retries import retried
from databricks.sdk.service.catalog import VolumeType
from databricks.sdk.service.sql import (
    CreateWarehouseRequestWarehouseType,
    EndpointInfoWarehouseType,
    SpotInstancePolicy,
)

import databricks.labs.remorph.resources
from databricks.labs.remorph.__about__ import __version__
from databricks.labs.remorph.config import (
    MorphConfig,
    ReconcileConfig,
    SQLGLOT_DIALECTS,
    DatabaseConfig,
    RemorphConfigs,
    ReconcileMetadataConfig,
)
from databricks.labs.remorph.helpers import db_sql
from databricks.labs.remorph.helpers.dashboard_publisher import DashboardPublisher
from databricks.labs.remorph.helpers.deployment import TableDeployer, JobDeployer
from databricks.labs.remorph.reconcile.constants import SourceType

logger = logging.getLogger(__name__)

PRODUCT_INFO = ProductInfo(__file__)
WAREHOUSE_PREFIX = "Remorph Transpiler Validation"


class WorkspaceInstaller:
    def __init__(self, ws: WorkspaceClient, installation: Installation, prompts: Prompts = Prompts()):
        if "DATABRICKS_RUNTIME_VERSION" in os.environ:
            msg = "WorkspaceInstaller is not supposed to be executed in Databricks Runtime"
            raise SystemExit(msg)
        self._ws = ws
        self._prompts = prompts
        self._catalog_setup = CatalogSetup(ws)
        self._product_info = ProductInfo.from_class(MorphConfig)
        self._install = InstallPrompts(ws, prompts)
        self._installation = installation

    def run(self):
        logger.info(f"Installing Remorph v{self._product_info.version()}")
        configs = self.configure()
        workspace_installation = WorkspaceInstallation(
            configs,
            self._installation,
            self._ws,
            self._prompts,
            verify_timeout=timedelta(minutes=2),
            product_info=self._product_info,
        )
        try:
            workspace_installation.run()
            self._save_configs(configs)
        except ManyError as err:
            if len(err.errs) == 1:
                raise err.errs[0] from None
            raise err
        return configs

    def configure(self) -> RemorphConfigs:
        """
        Returns the MorphConfig or ReconcileConfig If those are present on the Databricks Workspace,
         else prompts for the new Installation
        :return: RemorphConfigs
        """
        morph_config = None
        reconcile_config = None

        try:
            morph_config = self._installation.load(MorphConfig)
        except NotFound as err:
            logger.debug(f"Cannot find previous `transpile` installation: {err}")
        except (PermissionDenied, SerdeError, ValueError, AttributeError):
            logger.warning(f"Existing installation at {self._installation.install_folder()} is corrupted. Skipping...")

        try:
            reconcile_config = self._installation.load(ReconcileConfig)
        except NotFound as err:
            logger.debug(f"Cannot find previous `reconcile` installation: {err}")
        except (PermissionDenied, SerdeError, ValueError, AttributeError):
            logger.warning(f"Existing installation at {self._installation.install_folder()} is corrupted. Skipping...")

        if morph_config or reconcile_config:
            return RemorphConfigs(morph_config, reconcile_config)

        return self._configure_new_installation()

    def _save_configs(self, configs: RemorphConfigs):
        if configs.morph:
            self._save_and_open_config("transpile", configs.morph)
        if configs.reconcile:
            self._save_and_open_config("reconcile", configs.reconcile)

    def _save_and_open_config(self, module: str, config: MorphConfig | ReconcileConfig):
        logger.info(f"Saving the ** {module} ** configuration in Databricks Workspace")
        self._installation.save(config)
        ws_file_url = self._installation.workspace_link(config.__file__)
        if self._prompts.confirm(f"Open `{config.__file__}` in the browser and continue...?"):
            webbrowser.open(ws_file_url)

    def _configure_new_installation(self) -> RemorphConfigs:
        """
        Prompts for the new Installation and saves the configuration on the Databricks Workspace
        :return: RemorphConfigs
        """
        function_to_call = self._prompts.choice_from_dict(
            'Select a module to configure:',
            {
                'reconcile': self._install.reconcile_setup_prompts,
                'transpile': self._install.transpile_setup_prompts,
                'all': self._install.remorph_setup_prompts,
            },
        )
        configs = function_to_call()
        return configs


class CatalogSetup:
    def __init__(self, ws: WorkspaceClient):
        self._ws = ws

    def create(self, name: str):
        logger.debug(f"Creating Catalog `{name}`")
        catalog_info = self._ws.catalogs.create(name, comment="Created as part of Remorph installation")
        logger.info(f"Catalog `{name}` created")
        return catalog_info

    def get(self, name: str):
        try:
            logger.debug(f"Searching for Catalog `{name}`")
            catalog_info = self._ws.catalogs.get(name)
            logger.info(f"Catalog `{name}` found")
            return catalog_info.name
        except NotFound as err:
            logger.error(f"Cannot find Catalog: {err}")
            raise err
        except PermissionDenied as ex:
            logger.error(f"Permission Denied: {ex}")
            raise ex

    def create_schema(self, name: str, catalog_name: str):
        logger.debug(f"Creating Schema `{name}` in Catalog `{catalog_name}`")
        schema_info = self._ws.schemas.create(name, catalog_name, comment="Created as part of Remorph installation")
        logger.info(f"Created Schema `{name}` in Catalog `{catalog_name}`")
        return schema_info

    def get_schema(self, name: str):
        try:
            logger.debug(f"Searching for Schema `{name}`")
            schema_info = self._ws.schemas.get(name)
            logger.info(f"Schema `{name}` found")
            return schema_info.name
        except NotFound as err:
            logger.error(f"Cannot find Schema: {err}")
            raise err
        except PermissionDenied as ex:
            logger.error(f"Permission Denied: {ex}")
            raise ex


class InstallPrompts:
    def __init__(self, ws: WorkspaceClient, prompts: Prompts = Prompts()):
        self._source = None
        self._prompts = prompts
        self._ws = ws
        self._catalog_setup = CatalogSetup(ws)

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
            f"""Catalog `{catalog_name}` not found.\
                    \nDo you want to create a new one?"""
        )
        if not allow_catalog_creation:
            msg = "Catalog is needed to setup Remorph"
            raise SystemExit(msg)

        logger.info(f"Creating new Catalog `{catalog_name}`")
        self._catalog_setup.create(catalog_name)

    @retried(on=[NotFound], timeout=timedelta(minutes=5))
    def setup_schema(self, catalog_name: str, schema_name: str):
        allow_schema_creation = self._prompts.confirm(
            f"""Schema `{schema_name}` not found in Catalog `{catalog_name}`\
                    \nDo you want to create a new Schema?"""
        )
        if not allow_schema_creation:
            msg = "Schema is needed to setup Remorph"
            raise SystemExit(msg)

        logger.info(f"Creating new Schema `{catalog_name}.{schema_name}`")
        self._catalog_setup.create_schema(schema_name, catalog_name)

    def remorph_setup_prompts(self) -> RemorphConfigs:
        return RemorphConfigs(self.transpile_setup_prompts().morph, self.reconcile_setup_prompts().reconcile)

    def transpile_setup_prompts(self) -> RemorphConfigs:
        logger.info("\nPlease answer a few questions to configure remorph: ** transpile **")

        # default params
        catalog_name = "transpiler_test"
        schema_name = "convertor_test"
        ws_config = None

        source = self._prompts.choice("Select the source:", list(SQLGLOT_DIALECTS.keys()))

        input_sql = self._prompts.question("Enter Input SQL path (directory/file)")

        output_folder = self._prompts.question("Enter Output directory", default="transpiled")

        run_validation = self._prompts.confirm(
            "Would you like to validate the Syntax, Semantics of the transpiled queries?"
        )

        if run_validation:
            ws_config = self._configure_runtime()
            catalog_name = self._prompts.question("Enter Catalog for Validation")
            try:
                self._catalog_setup.get(catalog_name)
            except NotFound:
                self.setup_catalog(catalog_name)

            schema_name = self._prompts.question("Enter Schema for Validation")

            try:
                self._catalog_setup.get_schema(f"{catalog_name}.{schema_name}")
            except NotFound:
                self.setup_schema(catalog_name, schema_name)

        config = MorphConfig(
            source=source,
            skip_validation=(not run_validation),
            catalog_name=catalog_name,
            schema_name=schema_name,
            sdk_config=ws_config,
            mode="current",  # mode will not have a prompt as this is hidden flag
            input_sql=input_sql,
            output_folder=output_folder,
        )

        logger.info("Captured ** transpile **  configuration details !!!")

        return RemorphConfigs(config, None)

    def _prompt_for_reconcile_source_target_details(self, source):

        source_catalog = None
        if source == SourceType.SNOWFLAKE.value:
            source_catalog = self._prompts.question(f"Enter `{source.capitalize()}` Catalog name")

        schema_prompt = f"Enter `{source.capitalize()}` Schema name"
        if source in {SourceType.ORACLE.value, SourceType.SNOWFLAKE.value}:
            schema_prompt = f"Enter `{source.capitalize()}` Database name"

        source_schema = self._prompts.question(schema_prompt)

        target_catalog = self._prompts.question("Enter Databricks Catalog name")

        target_schema = self._prompts.question("Enter Databricks Schema name")

        return DatabaseConfig(
            source_schema=source_schema,
            target_catalog=target_catalog,
            target_schema=target_schema,
            source_catalog=source_catalog,
        )

    def _prompt_for_reconcile_metadata_config(self) -> ReconcileMetadataConfig:
        catalog = self._prompts.question("Enter Catalog name to store reconcile metadata", default="remorph")
        schema = self._prompts.question("Enter Schema name to store reconcile metadata", default="reconcile")
        metrics_config = ReconcileMetadataConfig(catalog=catalog, schema=schema)
        return metrics_config

    def reconcile_setup_prompts(self) -> RemorphConfigs:
        logger.info("\nPlease answer a few questions to configure remorph: ** reconcile **")

        data_source = self._prompts.choice(
            "Select the Data Source:",
            [SourceType.DATABRICKS.value, SourceType.SNOWFLAKE.value, SourceType.ORACLE.value],
        )
        report_type = self._prompts.choice("Select the Report Type:", ["data", "schema", "all", "row"])

        scope_name = self._prompts.question(
            f"Enter Secret Scope name to store `{data_source.capitalize()}` connection details / secrets",
            default=f"remorph_{data_source}",
        )

        db_config = self._prompt_for_reconcile_source_target_details(data_source)
        metadata_config = self._prompt_for_reconcile_metadata_config()

        reconcile_config = ReconcileConfig(
            data_source=data_source,
            report_type=report_type,
            secret_scope=scope_name,
            database_config=db_config,
            metadata_config=metadata_config,
        )

        logger.info("Captured ** reconcile **  configuration details !!!")

        return RemorphConfigs(None, reconcile_config)


class ReconciliationMetadataSetup:

    def __init__(
        self,
        ws: WorkspaceClient,
        reconcile_config: ReconcileConfig,
        catalog_setup: CatalogSetup,
        table_deployer: TableDeployer,
    ):
        self._ws = ws
        self._catalog_setup = catalog_setup
        self._table_deployer = table_deployer
        self._reconcile_config = reconcile_config
        self._reconcile_catalog = reconcile_config.metadata_config.catalog
        self._reconcile_schema = reconcile_config.metadata_config.schema

    def configure_catalog(self):
        try:
            self._catalog_setup.get(self._reconcile_catalog)
        except NotFound:
            logger.info(f"Creating new catalog {self._reconcile_catalog}")
            self._catalog_setup.create(self._reconcile_catalog)

    def configure_schema(self):
        try:
            self._catalog_setup.get_schema(f"{self._reconcile_catalog}.{self._reconcile_schema}")
        except NotFound:
            logger.info(f"Creating new schema {self._reconcile_catalog}.{self._reconcile_schema}")
            self._catalog_setup.create_schema(self._reconcile_schema, self._reconcile_catalog)

    def deploy_tables(self):
        logger.info("Deploying reconciliation metadata tables.")
        self._table_deployer.deploy_table("main", "queries/reconcile/installation/main.sql")
        self._table_deployer.deploy_table("metrics", "queries/reconcile/installation/metrics.sql")
        self._table_deployer.deploy_table("details", "queries/reconcile/installation/details.sql")

    def run(self):
        self.configure_catalog()
        self.configure_schema()
        self.deploy_tables()


class WorkspaceInstallation:
    def __init__(
        self,
        config: RemorphConfigs,
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

    def _create_reconcile_volume(self):
        all_volumes = self._ws.volumes.list(
            self._config.reconcile.metadata_config.catalog,
            self._config.reconcile.metadata_config.schema,
        )

        reconcile_volume_exists = False
        for volume in all_volumes:
            if volume.name == self._config.reconcile.metadata_config.volume:
                reconcile_volume_exists = True
                logger.info("Reconciliation Volume already exists.")
                break

        if not reconcile_volume_exists:
            logger.info("Creating Reconciliation Volume.")
            self._ws.volumes.create(
                self._config.reconcile.metadata_config.catalog,
                self._config.reconcile.metadata_config.schema,
                self._config.reconcile.metadata_config.volume,
                VolumeType.MANAGED,
            )

    def _create_reconcile_dashboard(self):
        dashboard_params = {
            "catalog": self._config.reconcile.metadata_config.catalog,
            "schema": self._config.reconcile.metadata_config.schema,
        }

        reconcile_dashboard_path = "dashboards/Remorph-Reconciliation.lvdash.json"
        dashboard_resource = files(databricks.labs.remorph.resources).joinpath(reconcile_dashboard_path)
        dashboard_publisher = DashboardPublisher(self._ws, self._installation)
        logger.info("Creating Reconciliation Dashboard.")
        with as_file(dashboard_resource) as dashboard_file:
            dashboard_publisher.create(dashboard_file, parameters=dashboard_params)

    def _configure_reconcile_metadata(self):
        morph_config = MorphConfig(
            source=self._config.reconcile.data_source,
            catalog_name=self._config.reconcile.metadata_config.catalog,
            schema_name=self._config.reconcile.metadata_config.schema,
        )
        sql_backend = db_sql.get_sql_backend(self._ws, morph_config)
        deployer = TableDeployer(
            sql_backend,
            self._config.reconcile.metadata_config.catalog,
            self._config.reconcile.metadata_config.schema,
        )
        setup = ReconciliationMetadataSetup(self._ws, self._config.reconcile, CatalogSetup(self._ws), deployer)
        setup.run()

    def _deploy_reconcile_job(self):
        job_deployer = JobDeployer(
            self._ws,
            self._installation,
            self._state,
            self._product_info,
        )
        job_id = job_deployer.deploy_job()
        self._config.reconcile.job_id = job_id

    def run(self):
        logger.info(f"Installing Remorph v{self._product_info.version()}")
        if self._config.reconcile:
            logger.info("Installing Reconcile components.")
            self._configure_reconcile_metadata()
            self._create_reconcile_volume()
            self._create_reconcile_dashboard()
            self._deploy_reconcile_job()

        logger.info("Installation completed successfully! Please refer to the documentation for the next steps.")


if __name__ == "__main__":
    logger = get_logger(__file__)
    logger.setLevel("INFO")
    if is_in_debug():
        logging.getLogger('databricks').setLevel(logging.DEBUG)

    w = WorkspaceClient(product="remorph", product_version=__version__)
    current = Installation.assume_user_home(w, PRODUCT_INFO.product_name())

    # TODO force_install
    installer = WorkspaceInstaller(w, current)
    installer.run()
