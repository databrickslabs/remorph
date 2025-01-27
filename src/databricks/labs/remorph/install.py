import dataclasses
from json import loads, dumps
import logging
import os
from shutil import rmtree, move
from subprocess import run, CalledProcessError
import sys
from typing import Any
from urllib import request
from urllib.error import URLError
import webbrowser
from datetime import datetime
from pathlib import Path

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
    TranspileConfig,
    ReconcileConfig,
    DatabaseConfig,
    RemorphConfigs,
    ReconcileMetadataConfig,
)
from databricks.labs.remorph.contexts.application import ApplicationContext
from databricks.labs.remorph.deployment.configurator import ResourceConfigurator
from databricks.labs.remorph.deployment.installation import WorkspaceInstallation
from databricks.labs.remorph.reconcile.constants import ReconReportType, ReconSourceType
from databricks.labs.remorph.transpiler.sqlglot.dialect_utils import SQLGLOT_DIALECTS

logger = logging.getLogger(__name__)

TRANSPILER_WAREHOUSE_PREFIX = "Remorph Transpiler Validation"
MODULES = sorted({"transpile", "reconcile", "all"})
LABS_PATH = Path.home() / ".databricks" / "labs"
TRANSPILERS_PATH = LABS_PATH / "remorph-transpilers"
OSS_TRANSPILER_NAME = "remorph-community-transpiler"
OSS_TRANSPILER_PYPI_NAME = f"databricks-labs-{OSS_TRANSPILER_NAME}"
MORPHEUS_TRANSPILER_NAME = "morpheus"
MORPHEUS_TRANSPILER_GROUP_NAME = "com.databricks.labs"


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
        self.install_community_transpiler()
        self.install_morpheus()
        logger.info(f"Installing Remorph v{self._product_info.version()}")
        if not config:
            config = self.configure()
        if self._is_testing():
            return config
        self._ws_installation.install(config)
        logger.info("Installation completed successfully! Please refer to the documentation for the next steps.")
        return config

    @classmethod
    def install_morpheus(cls):
        current_version = cls.get_installed_version(MORPHEUS_TRANSPILER_NAME)
        latest_version = cls.get_maven_version(MORPHEUS_TRANSPILER_GROUP_NAME, MORPHEUS_TRANSPILER_NAME)
        if current_version == latest_version:
            logger.info(f"Databricks Morpheus transpiler v{latest_version} already installed")
            return
        logger.info(f"Installing Databricks Morpheus transpiler v{latest_version}")
        product_path = TRANSPILERS_PATH / MORPHEUS_TRANSPILER_NAME
        if current_version is not None:
            product_path.rename(f"{MORPHEUS_TRANSPILER_NAME}-saved")
        install_path = product_path / "lib"
        install_path.mkdir()
        return_code = cls.download_from_maven(
            MORPHEUS_TRANSPILER_GROUP_NAME,
            MORPHEUS_TRANSPILER_NAME,
            latest_version,
            install_path / f"{MORPHEUS_TRANSPILER_NAME}.jar",
        )
        if return_code == 0:
            state_path = product_path / "state"
            state_path.mkdir()
            version_data = {"version": f"v{latest_version}", "date": str(datetime.now())}
            version_path = state_path / "version.json"
            version_path.write_text(dumps(version_data), "utf-8")
            logger.info(f"Successfully installed Databricks Morpheus transpiler v{latest_version}")
            if current_version is not None:
                rmtree(f"{product_path!s}-saved")
        else:
            logger.info(f"Failed to install Databricks Morpheus transpiler v{latest_version}")
            if current_version is not None:
                rmtree(str(product_path))
                renamed = Path(f"{product_path!s}-saved")
                renamed.rename(product_path.name)

    @classmethod
    def download_from_maven(cls, group_id: str, artifact_id: str, version: str, target: Path, extension="jar"):
        group_id = group_id.replace(".", "/")
        url = f"https://search.maven.org/remotecontent?filepath={group_id}/{artifact_id}/{version}/{artifact_id}-{version}.{extension}"
        try:
            path, message = request.urlretrieve(url)
            if path:
                move(path, str(target))
                return 0
            logger.error(message)
            return -1
        except URLError as e:
            logger.error("While downloading from maven", exc_info=e)
            return -1

    @classmethod
    def install_community_transpiler(cls):
        current_version = cls.get_installed_version(OSS_TRANSPILER_NAME)
        latest_version = cls.get_pypi_version(OSS_TRANSPILER_PYPI_NAME)
        if current_version == latest_version:
            logger.info(f"Remorph community transpiler v{latest_version} already installed")
            return
        logger.info(f"Installing Remorph community transpiler v{latest_version}")
        product_path = TRANSPILERS_PATH / OSS_TRANSPILER_NAME
        if current_version is not None:
            product_path.rename(f"{OSS_TRANSPILER_NAME}-saved")
        install_path = product_path / "lib"
        install_path.mkdir()
        args = ["pip", "install", OSS_TRANSPILER_PYPI_NAME, "-t", str(install_path)]
        state_path = product_path / "state"
        state_path.mkdir()
        version_data = {"version": f"v{latest_version}", "date": str(datetime.now())}
        version_path = state_path / "version.json"
        try:
            run(args, sys.stdin, sys.stdout, sys.stderr, check=True)
            version_path.write_text(dumps(version_data), "utf-8")
            logger.info(f"Successfully installed Remorph community transpiler v{latest_version}")
            if current_version is not None:
                rmtree(f"{product_path!s}-saved")
        except CalledProcessError as e:
            logger.info(f"Failed to install Remorph community transpiler v{latest_version}", exc_info=e)
            if current_version is not None:
                rmtree(str(product_path))
                renamed = Path(f"{product_path!s}-saved")
                renamed.rename(product_path.name)

    @classmethod
    def get_maven_version(cls, group_id: str, artifact_id: str) -> str | None:
        url = f"https://search.maven.org/solrsearch/select?q=g:{group_id}+AND+a:{artifact_id}&core=gav&rows=1&wt=json"
        with request.urlopen(url) as server:
            text = server.read()
        data: dict[str, Any] = loads(text)
        return data.get("response", {}).get('docs', [{}])[0].get("v", None)

    @classmethod
    def get_pypi_version(cls, product_name: str) -> str | None:
        with request.urlopen(f"https://pypi.org/pypi/{product_name}/json") as server:
            text = server.read()
        data: dict[str, Any] = loads(text)
        return data.get("info", {}).get('version', None)

    @classmethod
    def get_installed_version(cls, product_name: str, is_transpiler=True) -> str | None:
        product_path = (TRANSPILERS_PATH if is_transpiler else LABS_PATH) / product_name
        current_version_path = product_path / "state" / "version.json"
        if not current_version_path.exists():
            return None
        text = current_version_path.read_text("utf-8")
        data: dict[str, Any] = loads(text)
        version: str | None = data.get("version", None)
        if not version or not version.startswith("v"):
            return None
        return version[1:]

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

    def _configure_transpile(self) -> TranspileConfig:
        try:
            self._installation.load(TranspileConfig)
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

    def _configure_new_transpile_installation(self) -> TranspileConfig:
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

    def _prompt_for_new_transpile_installation(self) -> TranspileConfig:
        logger.info("Please answer a few questions to configure remorph `transpile`")
        transpiler = self._prompts.question("Enter path to the transpiler configuration file", default="sqlglot")
        source_dialect = self._prompts.choice("Select the source dialect:", list(SQLGLOT_DIALECTS.keys()))
        input_source = self._prompts.question("Enter input SQL path (directory/file)")
        output_folder = self._prompts.question("Enter output directory", default="transpiled")
        error_file_path = self._prompts.question("Enter error file path", default="errors.log")
        run_validation = self._prompts.confirm(
            "Would you like to validate the syntax and semantics of the transpiled queries?"
        )

        return TranspileConfig(
            transpiler_config_path=transpiler,
            source_dialect=source_dialect,
            skip_validation=(not run_validation),
            mode="current",  # mode will not have a prompt as this is a hidden flag
            input_source=input_source,
            output_folder=output_folder,
            error_file_path=error_file_path,
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

    def _save_config(self, config: TranspileConfig | ReconcileConfig):
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
