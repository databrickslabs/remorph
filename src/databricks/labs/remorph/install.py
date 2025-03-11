import abc
import dataclasses
import shutil
from collections.abc import Iterable
from json import loads, dumps
import logging
import os
from shutil import rmtree, move
from subprocess import run, CalledProcessError
import sys
from typing import Any, cast
from urllib import request
from urllib.error import URLError, HTTPError
import webbrowser
from datetime import datetime
from pathlib import Path

from databricks.labs.blueprint.installation import Installation
from databricks.labs.blueprint.installation import SerdeError
from databricks.labs.blueprint.installer import InstallState
from databricks.labs.blueprint.tui import Prompts
from databricks.labs.blueprint.wheels import ProductInfo
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import NotFound, PermissionDenied

from databricks.labs.remorph.config import (
    TranspileConfig,
    ReconcileConfig,
    DatabaseConfig,
    RemorphConfigs,
    ReconcileMetadataConfig,
    LSPConfigOptionV1,
    LSPPromptMethod,
)

from databricks.labs.remorph.deployment.configurator import ResourceConfigurator
from databricks.labs.remorph.deployment.installation import WorkspaceInstallation
from databricks.labs.remorph.reconcile.constants import ReconReportType, ReconSourceType
from databricks.labs.remorph.transpiler.lsp.lsp_engine import LSPConfig

logger = logging.getLogger(__name__)

TRANSPILER_WAREHOUSE_PREFIX = "Remorph Transpiler Validation"


class TranspilerInstaller(abc.ABC):

    @classmethod
    def labs_path(cls):
        return Path.home() / ".databricks" / "labs"

    @classmethod
    def transpilers_path(cls):
        return cls.labs_path() / "remorph-transpilers"

    @classmethod
    def resources_folder(cls):
        return Path(__file__).parent / "resources" / "transpilers"

    @classmethod
    def get_installed_version(cls, product_name: str, is_transpiler=True) -> str | None:
        product_path = (cls.transpilers_path() if is_transpiler else cls.labs_path()) / product_name
        current_version_path = product_path / "state" / "version.json"
        if not current_version_path.exists():
            return None
        text = current_version_path.read_text("utf-8")
        data: dict[str, Any] = loads(text)
        version: str | None = data.get("version", None)
        if not version or not version.startswith("v"):
            return None
        return version[1:]

    @classmethod
    def get_maven_version(cls, group_id: str, artifact_id: str) -> str | None:
        try:
            url = (
                f"https://search.maven.org/solrsearch/select?q=g:{group_id}+AND+a:{artifact_id}&core=gav&rows=1&wt=json"
            )
            with request.urlopen(url) as server:
                text = server.read()
            data: dict[str, Any] = loads(text)
            response = data.get("response", {})
            docs = response.get('docs', [{}])
            if len(docs) < 1:
                return None
            return docs[0].get("v", None)
        except HTTPError:
            return None

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
    def get_pypi_version(cls, product_name: str) -> str | None:
        try:
            with request.urlopen(f"https://pypi.org/pypi/{product_name}/json") as server:
                text = server.read()
            data: dict[str, Any] = loads(text)
            return data.get("info", {}).get('version', None)
        except HTTPError:
            return None

    @classmethod
    def install_from_pypi(cls, product_name: str, pypi_name: str):
        current_version = cls.get_installed_version(product_name)
        latest_version = cls.get_pypi_version(pypi_name)
        if current_version == latest_version:
            logger.info(f"{pypi_name} v{latest_version} already installed")
            return None
        logger.info(f"Installing {pypi_name} v{latest_version}")
        product_path = cls.transpilers_path() / product_name
        if current_version is not None:
            product_path.rename(f"{product_name}-saved")
        install_path = product_path / "lib"
        install_path.mkdir()
        args = ["pip", "install", pypi_name, "-t", str(install_path)]
        state_path = product_path / "state"
        state_path.mkdir()
        version_data = {"version": f"v{latest_version}", "date": str(datetime.now())}
        version_path = state_path / "version.json"
        try:
            run(args, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, check=True)
            version_path.write_text(dumps(version_data), "utf-8")
            logger.info(f"Successfully installed {pypi_name} v{latest_version}")
            if current_version is not None:
                rmtree(f"{product_path!s}-saved")
            return install_path
        except CalledProcessError as e:
            logger.info(f"Failed to install {pypi_name} v{latest_version}", exc_info=e)
            if current_version is not None:
                rmtree(str(product_path))
                renamed = Path(f"{product_path!s}-saved")
                renamed.rename(product_path.name)
            return None

    @classmethod
    def all_transpiler_configs(cls) -> dict[str, LSPConfig]:
        all_configs = cls._all_transpiler_configs()
        return {config.name: config for config in all_configs}

    @classmethod
    def all_transpiler_names(cls) -> set[str]:
        all_configs = cls.all_transpiler_configs()
        return set(all_configs.keys())

    @classmethod
    def all_dialects(cls):
        all_dialects: set[str] = set()
        for config in cls._all_transpiler_configs():
            all_dialects = all_dialects.union(config.remorph.dialects)
        return all_dialects

    @classmethod
    def transpilers_with_dialect(cls, dialect: str) -> set[str]:
        configs = filter(lambda cfg: dialect in cfg.remorph.dialects, cls.all_transpiler_configs().values())
        return set(config.name for config in configs)

    @classmethod
    def transpiler_config_path(cls, transpiler_name):
        config = cls.all_transpiler_configs().get(transpiler_name, None)
        if not config:
            raise ValueError(f"No such transpiler: {transpiler_name}")
        return f"{config.path!s}"

    @classmethod
    def transpiler_config_options(cls, transpiler_name, source_dialect) -> list[LSPConfigOptionV1]:
        config = cls.all_transpiler_configs().get(transpiler_name, None)
        if not config:
            return []  # gracefully returns an empty list, since this can only happen during testing
        return config.options.get(source_dialect, config.options.get("all", []))

    @classmethod
    def _all_transpiler_configs(cls) -> Iterable[LSPConfig]:
        path = cls.transpilers_path()
        if path.exists():
            all_files = os.listdir(path)
            for file in all_files:
                config = cls._transpiler_config(cls.transpilers_path() / file)
                if config:
                    yield config

    @classmethod
    def _transpiler_config(cls, path: Path) -> LSPConfig | None:
        if not path.is_dir() or not (path / "lib").is_dir():
            return None
        config_path = path / "lib" / "config.yml"
        if not config_path.is_file():
            return None
        try:
            return LSPConfig.load(config_path)
        except ValueError as e:
            logger.error(f"Could not load config: {path!s}", exc_info=e)
            return None


class RCTInstaller(TranspilerInstaller):
    RCT_TRANSPILER_NAME = "remorph-community-transpiler"
    RCT_TRANSPILER_PYPI_NAME = f"databricks-labs-{RCT_TRANSPILER_NAME}"

    @classmethod
    def install(cls):
        install_path = cls.install_from_pypi(cls.RCT_TRANSPILER_NAME, cls.RCT_TRANSPILER_PYPI_NAME)
        if install_path:
            config = TranspilerInstaller.resources_folder() / "rct" / "lib" / "config.yml"
            shutil.copyfile(str(config), str(install_path / "config.yml"))


class MorpheusInstaller(TranspilerInstaller):
    MORPHEUS_TRANSPILER_NAME = "morpheus"
    MORPHEUS_TRANSPILER_GROUP_NAME = "com.databricks.labs"

    @classmethod
    def install(cls):
        current_version = cls.get_installed_version(cls.MORPHEUS_TRANSPILER_NAME)
        latest_version = cls.get_maven_version(cls.MORPHEUS_TRANSPILER_GROUP_NAME, cls.MORPHEUS_TRANSPILER_NAME)
        if current_version == latest_version:
            logger.info(f"Databricks Morpheus transpiler v{latest_version} already installed")
            return
        if latest_version is None:
            return
        logger.info(f"Installing Databricks Morpheus transpiler v{latest_version}")
        product_path = cls.transpilers_path() / cls.MORPHEUS_TRANSPILER_NAME
        if current_version is not None:
            product_path.rename(f"{cls.MORPHEUS_TRANSPILER_NAME}-saved")
        install_path = product_path / "lib"
        install_path.mkdir()
        return_code = cls.download_from_maven(
            cls.MORPHEUS_TRANSPILER_GROUP_NAME,
            cls.MORPHEUS_TRANSPILER_NAME,
            latest_version,
            install_path / f"{cls.MORPHEUS_TRANSPILER_NAME}.jar",
        )
        if return_code == 0:
            state_path = product_path / "state"
            state_path.mkdir()
            version_data = {"version": f"v{latest_version}", "date": str(datetime.now())}
            version_path = state_path / "version.json"
            version_path.write_text(dumps(version_data), "utf-8")
            config = TranspilerInstaller.resources_folder() / "morpheus" / "lib" / "config.yml"
            shutil.copyfile(str(config), str(install_path / "config.yml"))
            logger.info(f"Successfully installed Databricks Morpheus transpiler v{latest_version}")
            if current_version is not None:
                rmtree(f"{product_path!s}-saved")
        else:
            logger.info(f"Failed to install Databricks Morpheus transpiler v{latest_version}")
            if current_version is not None:
                rmtree(str(product_path))
                renamed = Path(f"{product_path!s}-saved")
                renamed.rename(product_path.name)


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
        module: str,
        config: RemorphConfigs | None = None,
    ) -> RemorphConfigs:
        if module in {"transpile", "all"}:
            self.install_rct()
            self.install_morpheus()
        logger.info(f"Installing Remorph v{self._product_info.version()}")
        if not config:
            config = self.configure(module)
        if self._is_testing():
            return config
        self._ws_installation.install(config)
        logger.info("Installation completed successfully! Please refer to the documentation for the next steps.")
        return config

    @classmethod
    def install_rct(cls):
        RCTInstaller.install()

    @classmethod
    def install_morpheus(cls):
        MorpheusInstaller.install()

    def configure(self, module: str) -> RemorphConfigs:
        match module:
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
                raise ValueError(f"Invalid input: {module}")

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

    def _all_installed_dialects(self):
        return sorted(TranspilerInstaller.all_dialects())

    def _transpilers_with_dialect(self, dialect: str):
        return sorted(TranspilerInstaller.transpilers_with_dialect(dialect))

    def _transpiler_config_path(self, transpiler: str):
        return TranspilerInstaller.transpiler_config_path(transpiler)

    def _prompt_for_new_transpile_installation(self) -> TranspileConfig:
        install_later = "Set it later"
        # TODO tidy this up, logger might not display the below in console...
        logger.info("Please answer a few questions to configure remorph `transpile`")
        all_dialects = self._all_installed_dialects() + [install_later]
        source_dialect: str | None = self._prompts.choice("Select the source dialect:", all_dialects)
        if source_dialect == install_later:
            source_dialect = None
        transpiler_name = None
        transpiler_config_path = None
        if source_dialect:
            transpilers = self._transpilers_with_dialect(source_dialect)
            if len(transpilers) > 1:
                transpilers = transpilers + [install_later]
                transpiler_name = self._prompts.choice("Select the transpiler:", transpilers)
                if transpiler_name == install_later:
                    transpiler_name = None
            else:
                transpiler_name = next(t for t in transpilers)
                logger.info(f"Remorph will use the {transpiler_name} transpiler")
            if transpiler_name:
                transpiler_config_path = self._transpiler_config_path(transpiler_name)
        transpiler_options = None
        if transpiler_config_path:
            transpiler_options = self._prompt_for_transpiler_options(
                cast(str, transpiler_name), cast(str, source_dialect)
            )
        input_source: str | None = self._prompts.question(
            "Enter input SQL path (directory/file)", default=install_later
        )
        if input_source == install_later:
            input_source = None
        output_folder = self._prompts.question("Enter output directory", default="transpiled")
        error_file_path = self._prompts.question("Enter error file path", default="errors.log")
        run_validation = self._prompts.confirm(
            "Would you like to validate the syntax and semantics of the transpiled queries?"
        )

        return TranspileConfig(
            transpiler_config_path=transpiler_config_path,
            transpiler_options=transpiler_options,
            source_dialect=source_dialect,
            skip_validation=(not run_validation),
            input_source=input_source,
            output_folder=output_folder,
            error_file_path=error_file_path,
        )

    def _prompt_for_transpiler_options(self, transpiler_name: str, source_dialect: str) -> dict[str, Any] | None:
        config_options = TranspilerInstaller.transpiler_config_options(transpiler_name, source_dialect)
        if len(config_options) == 0:
            return None
        return {cfg.flag: self._prompt_for_transpiler_option(cfg) for cfg in config_options}

    def _prompt_for_transpiler_option(self, config_option: LSPConfigOptionV1) -> Any:
        if config_option.method == LSPPromptMethod.FORCE:
            return config_option.default
        if config_option.method == LSPPromptMethod.CONFIRM:
            return self._prompts.confirm(config_option.prompt)
        if config_option.method == LSPPromptMethod.QUESTION:
            return self._prompts.question(config_option.prompt, default=config_option.default)
        if config_option.method == LSPPromptMethod.CHOICE:
            return self._prompts.choice(config_option.prompt, cast(list[str], config_option.choices))
        raise ValueError(f"Unsupported prompt method: {config_option.method}")

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
