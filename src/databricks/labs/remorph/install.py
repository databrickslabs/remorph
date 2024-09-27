import dataclasses
import logging
import os
import webbrowser

from databricks.labs.blueprint.entrypoint import get_logger, is_in_debug
from databricks.labs.blueprint.installation import Installation
from databricks.labs.blueprint.installation import SerdeError
from databricks.labs.blueprint.installer import InstallState
from databricks.labs.blueprint.tui import Prompts
from databricks.labs.blueprint.wheels import ProductInfo
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import NotFound, PermissionDenied

from databricks.labs.remorph.__about__ import __version__
from databricks.labs.remorph.config import (
    MorphConfig,
    ReconcileConfig,
    SQLGLOT_DIALECTS,
    DatabaseConfig,
    RemorphConfigs,
    ReconcileMetadataConfig,
)
from databricks.labs.remorph.contexts.application import ApplicationContext
from databricks.labs.remorph.deployment.configurator import ResourceConfigurator
from databricks.labs.remorph.deployment.installation import WorkspaceInstallation
from databricks.labs.remorph.reconcile.constants import ReconReportType, ReconSourceType

logger = logging.getLogger(__name__)

TRANSPILER_WAREHOUSE_PREFIX = "Remorph Transpiler Validation"
MODULES = sorted({"transpile", "reconcile", "all"})


class WorkspaceInstaller:
    def __init__(
        self,
        ws: WorkspaceClient,
        prompts: Prompts,
        installation: Installation,
        install_state: InstallState,
        product_info: ProductInfo,
        resource_configurator: ResourceConfigurator,
        workspace_installation: WorkspaceInstallation,
        environ: dict[str, str] | None = None,
    ):
        self._ws = ws
        self._prompts = prompts
        self._installation = installation
        self._install_state = install_state
        self._product_info = product_info
        self._resource_configurator = resource_configurator
        self._ws_installation = workspace_installation

        if not environ:
            environ = dict(os.environ.items())

        if "DATABRICKS_RUNTIME_VERSION" in environ:
            msg = "WorkspaceInstaller is not supposed to be executed in Databricks Runtime"
            raise SystemExit(msg)

    def run(
        self,
        config: RemorphConfigs | None = None,
    ) -> RemorphConfigs:
        logger.info(f"Installing Remorph v{self._product_info.version()}")
        if not config:
            config = self.configure()
        if self._is_testing():
            return config
        self._ws_installation.install(config)
        logger.info("Installation completed successfully! Please refer to the documentation for the next steps.")
        return config

    def configure(self, module: str | None = None) -> RemorphConfigs:
        selected_module = module or self._prompts.choice("Select a module to configure:", MODULES)
        match selected_module:
            case "transpile":
                logger.info("Configuring remorph `transpile`.")
                return RemorphConfigs(self._configure_transpile(), None)
            case "reconcile":
                logger.info("Configuring remorph `reconcile`.")
                return RemorphConfigs(None, self._configure_reconcile())
            case "all":
                logger.info("Configuring remorph `transpile` and `reconcile`.")
                return RemorphConfigs(
                    self._configure_transpile(),
                    self._configure_reconcile(),
                )
            case _:
                raise ValueError(f"Invalid input: {selected_module}")

    def _is_testing(self):
        return self._product_info.product_name() != "remorph"

    def _configure_transpile(self) -> MorphConfig:
        try:
            self._installation.load(MorphConfig)
            logger.info("Remorph `transpile` is already installed on this workspace.")
            if not self._prompts.confirm("Do you want to override the existing installation?"):
                raise SystemExit(
                    "Remorph `transpile` is already installed and no override has been requested. Exiting..."
                )
        except NotFound:
            logger.info("Couldn't find existing `transpile` installation")
        except (PermissionDenied, SerdeError, ValueError, AttributeError):
            install_dir = self._installation.install_folder()
            logger.warning(
                f"Existing `transpile` installation at {install_dir} is corrupted. Continuing new installation..."
            )

        config = self._configure_new_transpile_installation()
        logger.info("Finished configuring remorph `transpile`.")
        return config

    def _configure_new_transpile_installation(self) -> MorphConfig:
        default_config = self._prompt_for_new_transpile_installation()
        runtime_config = None
        catalog_name = "remorph"
        schema_name = "transpiler"
        if not default_config.skip_validation:
            catalog_name = self._configure_catalog()
            schema_name = self._configure_schema(catalog_name, "transpile")
            self._has_necessary_access(catalog_name, schema_name)
            runtime_config = self._configure_runtime()

        config = dataclasses.replace(
            default_config,
            catalog_name=catalog_name,
            schema_name=schema_name,
            sdk_config=runtime_config,
        )
        self._save_config(config)
        return config

    def _prompt_for_new_transpile_installation(self) -> MorphConfig:
        logger.info("Please answer a few questions to configure remorph `transpile`")
        source = self._prompts.choice("Select the source:", list(SQLGLOT_DIALECTS.keys()))
        input_sql = self._prompts.question("Enter input SQL path (directory/file)")
        output_folder = self._prompts.question("Enter output directory", default="transpiled")
        run_validation = self._prompts.confirm(
            "Would you like to validate the syntax and semantics of the transpiled queries?"
        )

        return MorphConfig(
            source=source,
            skip_validation=(not run_validation),
            mode="current",  # mode will not have a prompt as this is a hidden flag
            input_sql=input_sql,
            output_folder=output_folder,
        )

    def _configure_catalog(
        self,
    ) -> str:
        return self._resource_configurator.prompt_for_catalog_setup()

    def _configure_schema(
        self,
        catalog: str,
        default_schema_name: str,
    ) -> str:
        return self._resource_configurator.prompt_for_schema_setup(
            catalog,
            default_schema_name,
        )

    def _configure_runtime(self) -> dict[str, str]:
        if self._prompts.confirm("Do you want to use SQL Warehouse for validation?"):
            warehouse_id = self._resource_configurator.prompt_for_warehouse_setup(TRANSPILER_WAREHOUSE_PREFIX)
            return {"warehouse_id": warehouse_id}

        if self._ws.config.cluster_id:
            logger.info(f"Using cluster {self._ws.config.cluster_id} for validation")
            return {"cluster_id": self._ws.config.cluster_id}

        cluster_id = self._prompts.question("Enter a valid cluster_id to proceed")
        return {"cluster_id": cluster_id}

    def _configure_reconcile(self) -> ReconcileConfig:
        try:
            self._installation.load(ReconcileConfig)
            logger.info("Remorph `reconcile` is already installed on this workspace.")
            if not self._prompts.confirm("Do you want to override the existing installation?"):
                raise SystemExit(
                    "Remorph `reconcile` is already installed and no override has been requested. Exiting..."
                )
        except NotFound:
            logger.info("Couldn't find existing `reconcile` installation")
        except (PermissionDenied, SerdeError, ValueError, AttributeError):
            install_dir = self._installation.install_folder()
            logger.warning(
                f"Existing `reconcile` installation at {install_dir} is corrupted. Continuing new installation..."
            )

        config = self._configure_new_reconcile_installation()
        logger.info("Finished configuring remorph `reconcile`.")
        return config

    def _configure_new_reconcile_installation(self) -> ReconcileConfig:
        default_config = self._prompt_for_new_reconcile_installation()
        self._save_config(default_config)
        return default_config

    def _prompt_for_new_reconcile_installation(self) -> ReconcileConfig:
        logger.info("Please answer a few questions to configure remorph `reconcile`")
        data_source = self._prompts.choice(
            "Select the Data Source:", [source_type.value for source_type in ReconSourceType]
        )
        report_type = self._prompts.choice(
            "Select the report type:", [report_type.value for report_type in ReconReportType]
        )
        scope_name = self._prompts.question(
            f"Enter Secret scope name to store `{data_source.capitalize()}` connection details / secrets",
            default=f"remorph_{data_source}",
        )

        db_config = self._prompt_for_reconcile_database_config(data_source)
        metadata_config = self._prompt_for_reconcile_metadata_config()

        return ReconcileConfig(
            data_source=data_source,
            report_type=report_type,
            secret_scope=scope_name,
            database_config=db_config,
            metadata_config=metadata_config,
        )

    def _prompt_for_reconcile_database_config(self, source) -> DatabaseConfig:
        source_catalog = None
        if source == ReconSourceType.SNOWFLAKE.value:
            source_catalog = self._prompts.question(f"Enter source catalog name for `{source.capitalize()}`")

        schema_prompt = f"Enter source schema name for `{source.capitalize()}`"
        if source in {ReconSourceType.ORACLE.value}:
            schema_prompt = f"Enter source database name for `{source.capitalize()}`"

        source_schema = self._prompts.question(schema_prompt)
        target_catalog = self._prompts.question("Enter target catalog name for Databricks")
        target_schema = self._prompts.question("Enter target schema name for Databricks")

        return DatabaseConfig(
            source_schema=source_schema,
            target_catalog=target_catalog,
            target_schema=target_schema,
            source_catalog=source_catalog,
        )

    def _prompt_for_reconcile_metadata_config(self) -> ReconcileMetadataConfig:
        logger.info("Configuring reconcile metadata.")
        catalog = self._configure_catalog()
        schema = self._configure_schema(
            catalog,
            "reconcile",
        )
        volume = self._configure_volume(catalog, schema, "reconcile_volume")
        self._has_necessary_access(catalog, schema, volume)
        return ReconcileMetadataConfig(catalog=catalog, schema=schema, volume=volume)

    def _configure_volume(
        self,
        catalog: str,
        schema: str,
        default_volume_name: str,
    ) -> str:
        return self._resource_configurator.prompt_for_volume_setup(
            catalog,
            schema,
            default_volume_name,
        )

    def _save_config(self, config: MorphConfig | ReconcileConfig):
        logger.info(f"Saving configuration file {config.__file__}")
        self._installation.save(config)
        ws_file_url = self._installation.workspace_link(config.__file__)
        if self._prompts.confirm(f"Open config file {ws_file_url} in the browser?"):
            webbrowser.open(ws_file_url)

    def _has_necessary_access(self, catalog_name: str, schema_name: str, volume_name: str | None = None):
        self._resource_configurator.has_necessary_access(catalog_name, schema_name, volume_name)


if __name__ == "__main__":
    logger = get_logger(__file__)
    logger.setLevel("INFO")
    if is_in_debug():
        logging.getLogger("databricks").setLevel(logging.DEBUG)

    app_context = ApplicationContext(WorkspaceClient(product="remorph", product_version=__version__))
    installer = WorkspaceInstaller(
        app_context.workspace_client,
        app_context.prompts,
        app_context.installation,
        app_context.install_state,
        app_context.product_info,
        app_context.resource_configurator,
        app_context.workspace_installation,
    )
    installer.run()
