from unittest.mock import create_autospec, patch

import pytest
from databricks.labs.blueprint.installation import MockInstallation
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import iam
from databricks.labs.blueprint.tui import MockPrompts
from databricks.labs.remorph.config import (
    RemorphConfigs,
    ReconcileConfig,
    DatabaseConfig,
    ReconcileMetadataConfig,
    LSPConfigOptionV1,
    LSPPromptMethod,
)
from databricks.labs.remorph.contexts.application import ApplicationContext
from databricks.labs.remorph.deployment.configurator import ResourceConfigurator
from databricks.labs.remorph.deployment.installation import WorkspaceInstallation
from databricks.labs.remorph.install import WorkspaceInstaller, TranspilerInstaller
from databricks.labs.remorph.config import TranspileConfig
from databricks.labs.blueprint.wheels import ProductInfo, WheelsV2
from databricks.labs.remorph.reconcile.constants import ReconSourceType, ReconReportType

RECONCILE_DATA_SOURCES = sorted([source_type.value for source_type in ReconSourceType])
RECONCILE_REPORT_TYPES = sorted([report_type.value for report_type in ReconReportType])


@pytest.fixture
def ws():
    w = create_autospec(WorkspaceClient)
    w.current_user.me.side_effect = lambda: iam.User(
        user_name="me@example.com", groups=[iam.ComplexValue(display="admins")]
    )
    return w

SET_IT_LATER = ["Set it later"]
ALL_INSTALLED_DIALECTS_NO_LATER = ["tsql", "snowflake"]
ALL_INSTALLED_DIALECTS = sorted(ALL_INSTALLED_DIALECTS_NO_LATER + SET_IT_LATER )
TRANSPILERS_FOR_SNOWFLAKE_NO_LATER = ["Remorph Community Transpiler", "Morpheus"]
TRANSPILERS_FOR_SNOWFLAKE = sorted(TRANSPILERS_FOR_SNOWFLAKE_NO_LATER + SET_IT_LATER)
PATH_TO_TRANSPILER_CONFIG = "/some/path/to/config.yml"


@pytest.fixture()
def ws_installer():

    class TestWorkspaceInstaller(WorkspaceInstaller):
        # TODO the below methods currently raise a 404 because the artifacts don't exist yet
        # TODO remove this once they are available !!!
        @classmethod
        def install_rct(cls):
            pass

        @classmethod
        def install_morpheus(cls):
            pass

        def _all_installed_dialects(self):
            return ALL_INSTALLED_DIALECTS_NO_LATER

        def _transpilers_with_dialect(self, dialect):
            return TRANSPILERS_FOR_SNOWFLAKE_NO_LATER

        def _transpiler_config_path(self, transpiler):
            return PATH_TO_TRANSPILER_CONFIG

    def installer(*args, **kwargs) -> WorkspaceInstaller:
        return TestWorkspaceInstaller(*args, **kwargs)

    yield installer


def test_workspace_installer_run_raise_error_in_dbr(ws):
    ctx = ApplicationContext(ws)
    environ = {"DATABRICKS_RUNTIME_VERSION": "8.3.x-scala2.12"}
    with pytest.raises(SystemExit):
        WorkspaceInstaller(
            ctx.workspace_client,
            ctx.prompts,
            ctx.installation,
            ctx.install_state,
            ctx.product_info,
            ctx.resource_configurator,
            ctx.workspace_installation,
            environ=environ,
        )


def test_workspace_installer_run_install_not_called_in_test(ws_installer, ws):
    ws_installation = create_autospec(WorkspaceInstallation)
    ctx = ApplicationContext(ws)
    ctx.replace(
        product_info=ProductInfo.for_testing(RemorphConfigs),
        resource_configurator=create_autospec(ResourceConfigurator),
        workspace_installation=ws_installation,
    )

    provided_config = RemorphConfigs()
    workspace_installer = ws_installer(
        ctx.workspace_client,
        ctx.prompts,
        ctx.installation,
        ctx.install_state,
        ctx.product_info,
        ctx.resource_configurator,
        ctx.workspace_installation,
    )

    returned_config = workspace_installer.run(module="transpile", config=provided_config)

    assert returned_config == provided_config
    ws_installation.install.assert_not_called()


def test_workspace_installer_run_install_called_with_provided_config(ws_installer, ws):
    ws_installation = create_autospec(WorkspaceInstallation)
    ctx = ApplicationContext(ws)
    ctx.replace(
        resource_configurator=create_autospec(ResourceConfigurator),
        workspace_installation=ws_installation,
    )
    provided_config = RemorphConfigs()
    workspace_installer = ws_installer(
        ctx.workspace_client,
        ctx.prompts,
        ctx.installation,
        ctx.install_state,
        ctx.product_info,
        ctx.resource_configurator,
        ctx.workspace_installation,
    )

    returned_config = workspace_installer.run(module="transpile", config=provided_config)

    assert returned_config == provided_config
    ws_installation.install.assert_called_once_with(provided_config)


def test_configure_error_if_invalid_module_selected(ws):
    ctx = ApplicationContext(ws)
    ctx.replace(
        resource_configurator=create_autospec(ResourceConfigurator),
        workspace_installation=create_autospec(WorkspaceInstallation),
    )
    workspace_installer = WorkspaceInstaller(
        ctx.workspace_client,
        ctx.prompts,
        ctx.installation,
        ctx.install_state,
        ctx.product_info,
        ctx.resource_configurator,
        ctx.workspace_installation,
    )

    with pytest.raises(ValueError):
        workspace_installer.configure(module="invalid_module")


def test_workspace_installer_run_install_called_with_generated_config(ws_installer, ws):
    idx = ALL_INSTALLED_DIALECTS.index("snowflake")
    prompts = MockPrompts(
        {
            r"Do you want to override the existing installation?": "no",
            r"Select the source dialect": ALL_INSTALLED_DIALECTS.index("snowflake"),
            r"Select the transpiler": TRANSPILERS_FOR_SNOWFLAKE.index("Morpheus"),
            r"Enter input SQL path.*": "/tmp/queries/snow",
            r"Enter output directory.*": "/tmp/queries/databricks",
            r"Enter error file path.*": "/tmp/queries/errors.log",
            r"Would you like to validate.*": "no",
            r"Open .* in the browser?": "no",
        }
    )
    installation = MockInstallation()
    ctx = ApplicationContext(ws)
    ctx.replace(
        prompts=prompts,
        installation=installation,
        resource_configurator=create_autospec(ResourceConfigurator),
        workspace_installation=create_autospec(WorkspaceInstallation),
    )

    workspace_installer = ws_installer(
        ctx.workspace_client,
        ctx.prompts,
        ctx.installation,
        ctx.install_state,
        ctx.product_info,
        ctx.resource_configurator,
        ctx.workspace_installation,
    )
    workspace_installer.run("transpile")
    installation.assert_file_written(
        "config.yml",
        {
            "catalog_name": "remorph",
            "transpiler_config_path": PATH_TO_TRANSPILER_CONFIG,
            "source_dialect": "snowflake",
            "input_source": "/tmp/queries/snow",
            "output_folder": "/tmp/queries/databricks",
            "error_file_path": "/tmp/queries/errors.log",
            "schema_name": "transpiler",
            "skip_validation": True,
            "version": 3,
        },
    )


def test_configure_transpile_no_existing_installation(ws_installer, ws):
    prompts = MockPrompts(
        {
            r"Do you want to override the existing installation?": "no",
            r"Select the source dialect": ALL_INSTALLED_DIALECTS.index("snowflake"),
            r"Select the transpiler": TRANSPILERS_FOR_SNOWFLAKE.index("Morpheus"),
            r"Enter input SQL path.*": "/tmp/queries/snow",
            r"Enter output directory.*": "/tmp/queries/databricks",
            r"Enter error file path.*": "/tmp/queries/errors.log",
            r"Would you like to validate.*": "no",
            r"Open .* in the browser?": "no",
        }
    )
    installation = MockInstallation()
    ctx = ApplicationContext(ws)
    ctx.replace(
        prompts=prompts,
        installation=installation,
        resource_configurator=create_autospec(ResourceConfigurator),
        workspace_installation=create_autospec(WorkspaceInstallation),
    )
    workspace_installer = ws_installer(
        ctx.workspace_client,
        ctx.prompts,
        ctx.installation,
        ctx.install_state,
        ctx.product_info,
        ctx.resource_configurator,
        ctx.workspace_installation,
    )

    config = workspace_installer.configure(module="transpile")
    expected_morph_config = TranspileConfig(
        transpiler_config_path=PATH_TO_TRANSPILER_CONFIG,
        source_dialect="snowflake",
        input_source="/tmp/queries/snow",
        output_folder="/tmp/queries/databricks",
        error_file_path="/tmp/queries/errors.log",
        skip_validation=True,
        catalog_name="remorph",
        schema_name="transpiler",
    )
    expected_config = RemorphConfigs(transpile=expected_morph_config)
    assert config == expected_config
    installation.assert_file_written(
        "config.yml",
        {
            "catalog_name": "remorph",
            "transpiler_config_path": PATH_TO_TRANSPILER_CONFIG,
            "input_source": "/tmp/queries/snow",
            "output_folder": "/tmp/queries/databricks",
            "error_file_path": "/tmp/queries/errors.log",
            "schema_name": "transpiler",
            "skip_validation": True,
            "source_dialect": "snowflake",
            "version": 3,
        },
    )


def test_configure_transpile_installation_no_override(ws):
    prompts = MockPrompts(
        {
            r"Do you want to override the existing installation?": "no",
        }
    )
    ctx = ApplicationContext(ws)
    ctx.replace(
        prompts=prompts,
        resource_configurator=create_autospec(ResourceConfigurator),
        workspace_installation=create_autospec(WorkspaceInstallation),
        installation=MockInstallation(
            {
                "config.yml": {
                    "transpiler_config_path": PATH_TO_TRANSPILER_CONFIG,
                    "source_dialect": "snowflake",
                    "catalog_name": "transpiler_test",
                    "input_source": "sf_queries",
                    "output_folder": "out_dir",
                    "schema_name": "convertor_test",
                    "sdk_config": {
                        "warehouse_id": "abc",
                    },
                    "version": 3,
                }
            }
        ),
    )

    workspace_installer = WorkspaceInstaller(
        ctx.workspace_client,
        ctx.prompts,
        ctx.installation,
        ctx.install_state,
        ctx.product_info,
        ctx.resource_configurator,
        ctx.workspace_installation,
    )
    with pytest.raises(SystemExit):
        workspace_installer.configure(module="transpile")


def test_configure_transpile_installation_config_error_continue_install(ws_installer, ws):
    prompts = MockPrompts(
        {
            r"Do you want to override the existing installation?": "no",
            r"Select the source dialect": ALL_INSTALLED_DIALECTS.index("snowflake"),
            r"Select the transpiler": TRANSPILERS_FOR_SNOWFLAKE.index("Morpheus"),
            r"Enter input SQL path.*": "/tmp/queries/snow",
            r"Enter output directory.*": "/tmp/queries/databricks",
            r"Enter error file path.*": "/tmp/queries/errors.log",
            r"Would you like to validate.*": "no",
            r"Open .* in the browser?": "no",
        }
    )
    installation = MockInstallation(
        {
            "config.yml": {
                "invalid_transpiler": "some value",  # Invalid key
                "source_dialect": "snowflake",
                "catalog_name": "transpiler_test",
                "input_source": "sf_queries",
                "output_folder": "out_dir",
                "error_file_path": "error_log",
                "schema_name": "convertor_test",
                "sdk_config": {
                    "warehouse_id": "abc",
                },
                "version": 3,
            }
        }
    )
    ctx = ApplicationContext(ws)
    ctx.replace(
        prompts=prompts,
        installation=installation,
        resource_configurator=create_autospec(ResourceConfigurator),
        workspace_installation=create_autospec(WorkspaceInstallation),
    )
    workspace_installer = ws_installer(
        ctx.workspace_client,
        ctx.prompts,
        ctx.installation,
        ctx.install_state,
        ctx.product_info,
        ctx.resource_configurator,
        ctx.workspace_installation,
    )

    config = workspace_installer.configure(module="transpile")

    expected_morph_config = TranspileConfig(
        transpiler_config_path=PATH_TO_TRANSPILER_CONFIG,
        source_dialect="snowflake",
        input_source="/tmp/queries/snow",
        output_folder="/tmp/queries/databricks",
        error_file_path="/tmp/queries/errors.log",
        skip_validation=True,
        catalog_name="remorph",
        schema_name="transpiler",
    )
    expected_config = RemorphConfigs(transpile=expected_morph_config)
    assert config == expected_config
    installation.assert_file_written(
        "config.yml",
        {
            "transpiler_config_path": PATH_TO_TRANSPILER_CONFIG,
            "catalog_name": "remorph",
            "input_source": "/tmp/queries/snow",
            "output_folder": "/tmp/queries/databricks",
            "error_file_path": "/tmp/queries/errors.log",
            "schema_name": "transpiler",
            "skip_validation": True,
            "source_dialect": "snowflake",
            "version": 3,
        },
    )


@patch("webbrowser.open")
def test_configure_transpile_installation_with_no_validation(ws, ws_installer):
    prompts = MockPrompts(
        {
            r"Select the source dialect": ALL_INSTALLED_DIALECTS.index("snowflake"),
            r"Select the transpiler": TRANSPILERS_FOR_SNOWFLAKE.index("Morpheus"),
            r"Enter input SQL path.*": "/tmp/queries/snow",
            r"Enter output directory.*": "/tmp/queries/databricks",
            r"Enter error file path.*": "/tmp/queries/errors.log",
            r"Would you like to validate.*": "no",
            r"Open .* in the browser?": "yes",
        }
    )
    installation = MockInstallation()
    ctx = ApplicationContext(ws)
    ctx.replace(
        prompts=prompts,
        installation=installation,
        resource_configurator=create_autospec(ResourceConfigurator),
        workspace_installation=create_autospec(WorkspaceInstallation),
    )

    workspace_installer = ws_installer(
        ctx.workspace_client,
        ctx.prompts,
        ctx.installation,
        ctx.install_state,
        ctx.product_info,
        ctx.resource_configurator,
        ctx.workspace_installation,
    )

    config = workspace_installer.configure(module="transpile")

    expected_morph_config = TranspileConfig(
        transpiler_config_path=PATH_TO_TRANSPILER_CONFIG,
        source_dialect="snowflake",
        input_source="/tmp/queries/snow",
        output_folder="/tmp/queries/databricks",
        error_file_path="/tmp/queries/errors.log",
        skip_validation=True,
        catalog_name="remorph",
        schema_name="transpiler",
    )
    expected_config = RemorphConfigs(transpile=expected_morph_config)
    assert config == expected_config
    installation.assert_file_written(
        "config.yml",
        {
            "transpiler_config_path": PATH_TO_TRANSPILER_CONFIG,
            "catalog_name": "remorph",
            "input_source": "/tmp/queries/snow",
            "output_folder": "/tmp/queries/databricks",
            "error_file_path": "/tmp/queries/errors.log",
            "schema_name": "transpiler",
            "skip_validation": True,
            "source_dialect": "snowflake",
            "version": 3,
        },
    )


def test_configure_transpile_installation_with_validation_and_cluster_id_in_config(ws_installer, ws):
    prompts = MockPrompts(
        {
            r"Select the source dialect": ALL_INSTALLED_DIALECTS.index("snowflake"),
            r"Select the transpiler": TRANSPILERS_FOR_SNOWFLAKE.index("Morpheus"),
            r"Enter input SQL path.*": "/tmp/queries/snow",
            r"Enter output directory.*": "/tmp/queries/databricks",
            r"Enter error file path.*": "/tmp/queries/errors.log",
            r"Would you like to validate.*": "yes",
            r"Do you want to use SQL Warehouse for validation?": "no",
            r"Open .* in the browser?": "no",
        }
    )
    installation = MockInstallation()
    ws.config.cluster_id = "1234"

    resource_configurator = create_autospec(ResourceConfigurator)
    resource_configurator.prompt_for_catalog_setup.return_value = "remorph_test"
    resource_configurator.prompt_for_schema_setup.return_value = "transpiler_test"

    ctx = ApplicationContext(ws)
    ctx.replace(
        prompts=prompts,
        installation=installation,
        resource_configurator=resource_configurator,
        workspace_installation=create_autospec(WorkspaceInstallation),
    )

    workspace_installer = ws_installer(
        ctx.workspace_client,
        ctx.prompts,
        ctx.installation,
        ctx.install_state,
        ctx.product_info,
        ctx.resource_configurator,
        ctx.workspace_installation,
    )

    config = workspace_installer.configure(module="transpile")

    expected_config = RemorphConfigs(
        transpile=TranspileConfig(
            transpiler_config_path=PATH_TO_TRANSPILER_CONFIG,
            source_dialect="snowflake",
            input_source="/tmp/queries/snow",
            output_folder="/tmp/queries/databricks",
            error_file_path="/tmp/queries/errors.log",
            catalog_name="remorph_test",
            schema_name="transpiler_test",
            sdk_config={"cluster_id": "1234"},
        )
    )
    assert config == expected_config
    installation.assert_file_written(
        "config.yml",
        {
            "transpiler_config_path": PATH_TO_TRANSPILER_CONFIG,
            "catalog_name": "remorph_test",
            "input_source": "/tmp/queries/snow",
            "output_folder": "/tmp/queries/databricks",
            "error_file_path": "/tmp/queries/errors.log",
            "schema_name": "transpiler_test",
            "sdk_config": {"cluster_id": "1234"},
            "source_dialect": "snowflake",
            "version": 3,
        },
    )


def test_configure_transpile_installation_with_validation_and_cluster_id_from_prompt(ws_installer, ws):
    prompts = MockPrompts(
        {
            r"Select the source dialect": ALL_INSTALLED_DIALECTS.index("snowflake"),
            r"Select the transpiler": TRANSPILERS_FOR_SNOWFLAKE.index("Morpheus"),
            r"Enter input SQL path.*": "/tmp/queries/snow",
            r"Enter output directory.*": "/tmp/queries/databricks",
            r"Enter error file path.*": "/tmp/queries/errors.log",
            r"Would you like to validate.*": "yes",
            r"Do you want to use SQL Warehouse for validation?": "no",
            r"Enter a valid cluster_id to proceed": "1234",
            r"Open .* in the browser?": "no",
        }
    )
    installation = MockInstallation()
    ws.config.cluster_id = None

    resource_configurator = create_autospec(ResourceConfigurator)
    resource_configurator.prompt_for_catalog_setup.return_value = "remorph_test"
    resource_configurator.prompt_for_schema_setup.return_value = "transpiler_test"

    ctx = ApplicationContext(ws)
    ctx.replace(
        prompts=prompts,
        installation=installation,
        resource_configurator=resource_configurator,
        workspace_installation=create_autospec(WorkspaceInstallation),
    )

    workspace_installer = ws_installer(
        ctx.workspace_client,
        ctx.prompts,
        ctx.installation,
        ctx.install_state,
        ctx.product_info,
        ctx.resource_configurator,
        ctx.workspace_installation,
    )

    config = workspace_installer.configure(module="transpile")

    expected_config = RemorphConfigs(
        transpile=TranspileConfig(
            transpiler_config_path=PATH_TO_TRANSPILER_CONFIG,
            source_dialect="snowflake",
            input_source="/tmp/queries/snow",
            output_folder="/tmp/queries/databricks",
            error_file_path="/tmp/queries/errors.log",
            catalog_name="remorph_test",
            schema_name="transpiler_test",
            sdk_config={"cluster_id": "1234"},
        )
    )
    assert config == expected_config
    installation.assert_file_written(
        "config.yml",
        {
            "transpiler_config_path": PATH_TO_TRANSPILER_CONFIG,
            "catalog_name": "remorph_test",
            "input_source": "/tmp/queries/snow",
            "output_folder": "/tmp/queries/databricks",
            "error_file_path": "/tmp/queries/errors.log",
            "schema_name": "transpiler_test",
            "sdk_config": {"cluster_id": "1234"},
            "source_dialect": "snowflake",
            "version": 3,
        },
    )


def test_configure_transpile_installation_with_validation_and_warehouse_id_from_prompt(ws_installer, ws):
    prompts = MockPrompts(
        {
            r"Select the source dialect": ALL_INSTALLED_DIALECTS.index("snowflake"),
            r"Select the transpiler": TRANSPILERS_FOR_SNOWFLAKE.index("Morpheus"),
            r"Enter input SQL path.*": "/tmp/queries/snow",
            r"Enter output directory.*": "/tmp/queries/databricks",
            r"Enter error file path.*": "/tmp/queries/errors.log",
            r"Would you like to validate.*": "yes",
            r"Do you want to use SQL Warehouse for validation?": "yes",
            r"Open .* in the browser?": "no",
        }
    )
    installation = MockInstallation()
    resource_configurator = create_autospec(ResourceConfigurator)
    resource_configurator.prompt_for_catalog_setup.return_value = "remorph_test"
    resource_configurator.prompt_for_schema_setup.return_value = "transpiler_test"
    resource_configurator.prompt_for_warehouse_setup.return_value = "w_id"

    ctx = ApplicationContext(ws)
    ctx.replace(
        prompts=prompts,
        installation=installation,
        resource_configurator=resource_configurator,
        workspace_installation=create_autospec(WorkspaceInstallation),
    )

    workspace_installer = ws_installer(
        ctx.workspace_client,
        ctx.prompts,
        ctx.installation,
        ctx.install_state,
        ctx.product_info,
        ctx.resource_configurator,
        ctx.workspace_installation,
    )

    config = workspace_installer.configure(module="transpile")

    expected_config = RemorphConfigs(
        transpile=TranspileConfig(
            transpiler_config_path=PATH_TO_TRANSPILER_CONFIG,
            source_dialect="snowflake",
            input_source="/tmp/queries/snow",
            output_folder="/tmp/queries/databricks",
            error_file_path="/tmp/queries/errors.log",
            catalog_name="remorph_test",
            schema_name="transpiler_test",
            sdk_config={"warehouse_id": "w_id"},
        )
    )
    assert config == expected_config
    installation.assert_file_written(
        "config.yml",
        {
            "transpiler_config_path": PATH_TO_TRANSPILER_CONFIG,
            "catalog_name": "remorph_test",
            "input_source": "/tmp/queries/snow",
            "output_folder": "/tmp/queries/databricks",
            "error_file_path": "/tmp/queries/errors.log",
            "schema_name": "transpiler_test",
            "sdk_config": {"warehouse_id": "w_id"},
            "source_dialect": "snowflake",
            "version": 3,
        },
    )


def test_configure_reconcile_installation_no_override(ws):
    prompts = MockPrompts(
        {
            r"Do you want to override the existing installation?": "no",
        }
    )
    ctx = ApplicationContext(ws)
    ctx.replace(
        prompts=prompts,
        resource_configurator=create_autospec(ResourceConfigurator),
        workspace_installation=create_autospec(WorkspaceInstallation),
        installation=MockInstallation(
            {
                "reconcile.yml": {
                    "data_source": "snowflake",
                    "report_type": "all",
                    "secret_scope": "remorph_snowflake",
                    "database_config": {
                        "source_catalog": "snowflake_sample_data",
                        "source_schema": "tpch_sf1000",
                        "target_catalog": "tpch",
                        "target_schema": "1000gb",
                    },
                    "metadata_config": {
                        "catalog": "remorph",
                        "schema": "reconcile",
                        "volume": "reconcile_volume",
                    },
                    "version": 1,
                }
            }
        ),
    )
    workspace_installer = WorkspaceInstaller(
        ctx.workspace_client,
        ctx.prompts,
        ctx.installation,
        ctx.install_state,
        ctx.product_info,
        ctx.resource_configurator,
        ctx.workspace_installation,
    )
    with pytest.raises(SystemExit):
        workspace_installer.configure(module="reconcile")


def test_configure_reconcile_installation_config_error_continue_install(ws):
    prompts = MockPrompts(
        {
            r"Select the Data Source": RECONCILE_DATA_SOURCES.index("oracle"),
            r"Select the report type": RECONCILE_REPORT_TYPES.index("all"),
            r"Enter Secret scope name to store .* connection details / secrets": "remorph_oracle",
            r"Enter source database name for .*": "tpch_sf1000",
            r"Enter target catalog name for Databricks": "tpch",
            r"Enter target schema name for Databricks": "1000gb",
            r"Open .* in the browser?": "no",
        }
    )
    installation = MockInstallation(
        {
            "reconcile.yml": {
                "source_dialect": "oracle",  # Invalid key
                "report_type": "all",
                "secret_scope": "remorph_oracle",
                "database_config": {
                    "source_schema": "tpch_sf1000",
                    "target_catalog": "tpch",
                    "target_schema": "1000gb",
                },
                "metadata_config": {
                    "catalog": "remorph",
                    "schema": "reconcile",
                    "volume": "reconcile_volume",
                },
                "version": 1,
            }
        }
    )

    resource_configurator = create_autospec(ResourceConfigurator)
    resource_configurator.prompt_for_catalog_setup.return_value = "remorph"
    resource_configurator.prompt_for_schema_setup.return_value = "reconcile"
    resource_configurator.prompt_for_volume_setup.return_value = "reconcile_volume"

    ctx = ApplicationContext(ws)
    ctx.replace(
        prompts=prompts,
        installation=installation,
        resource_configurator=resource_configurator,
        workspace_installation=create_autospec(WorkspaceInstallation),
    )

    workspace_installer = WorkspaceInstaller(
        ctx.workspace_client,
        ctx.prompts,
        ctx.installation,
        ctx.install_state,
        ctx.product_info,
        ctx.resource_configurator,
        ctx.workspace_installation,
    )
    config = workspace_installer.configure(module="reconcile")

    expected_config = RemorphConfigs(
        reconcile=ReconcileConfig(
            data_source="oracle",
            report_type="all",
            secret_scope="remorph_oracle",
            database_config=DatabaseConfig(
                source_schema="tpch_sf1000",
                target_catalog="tpch",
                target_schema="1000gb",
            ),
            metadata_config=ReconcileMetadataConfig(
                catalog="remorph",
                schema="reconcile",
                volume="reconcile_volume",
            ),
        )
    )
    assert config == expected_config
    installation.assert_file_written(
        "reconcile.yml",
        {
            "data_source": "oracle",
            "report_type": "all",
            "secret_scope": "remorph_oracle",
            "database_config": {
                "source_schema": "tpch_sf1000",
                "target_catalog": "tpch",
                "target_schema": "1000gb",
            },
            "metadata_config": {
                "catalog": "remorph",
                "schema": "reconcile",
                "volume": "reconcile_volume",
            },
            "version": 1,
        },
    )


@patch("webbrowser.open")
def test_configure_reconcile_no_existing_installation(ws):
    prompts = MockPrompts(
        {
            r"Select the Data Source": RECONCILE_DATA_SOURCES.index("snowflake"),
            r"Select the report type": RECONCILE_REPORT_TYPES.index("all"),
            r"Enter Secret scope name to store .* connection details / secrets": "remorph_snowflake",
            r"Enter source catalog name for .*": "snowflake_sample_data",
            r"Enter source schema name for .*": "tpch_sf1000",
            r"Enter target catalog name for Databricks": "tpch",
            r"Enter target schema name for Databricks": "1000gb",
            r"Open .* in the browser?": "yes",
        }
    )
    installation = MockInstallation()
    resource_configurator = create_autospec(ResourceConfigurator)
    resource_configurator.prompt_for_catalog_setup.return_value = "remorph"
    resource_configurator.prompt_for_schema_setup.return_value = "reconcile"
    resource_configurator.prompt_for_volume_setup.return_value = "reconcile_volume"

    ctx = ApplicationContext(ws)
    ctx.replace(
        prompts=prompts,
        installation=installation,
        resource_configurator=resource_configurator,
        workspace_installation=create_autospec(WorkspaceInstallation),
    )

    workspace_installer = WorkspaceInstaller(
        ctx.workspace_client,
        ctx.prompts,
        ctx.installation,
        ctx.install_state,
        ctx.product_info,
        ctx.resource_configurator,
        ctx.workspace_installation,
    )
    config = workspace_installer.configure(module="reconcile")

    expected_config = RemorphConfigs(
        reconcile=ReconcileConfig(
            data_source="snowflake",
            report_type="all",
            secret_scope="remorph_snowflake",
            database_config=DatabaseConfig(
                source_schema="tpch_sf1000",
                target_catalog="tpch",
                target_schema="1000gb",
                source_catalog="snowflake_sample_data",
            ),
            metadata_config=ReconcileMetadataConfig(
                catalog="remorph",
                schema="reconcile",
                volume="reconcile_volume",
            ),
        )
    )
    assert config == expected_config
    installation.assert_file_written(
        "reconcile.yml",
        {
            "data_source": "snowflake",
            "report_type": "all",
            "secret_scope": "remorph_snowflake",
            "database_config": {
                "source_catalog": "snowflake_sample_data",
                "source_schema": "tpch_sf1000",
                "target_catalog": "tpch",
                "target_schema": "1000gb",
            },
            "metadata_config": {
                "catalog": "remorph",
                "schema": "reconcile",
                "volume": "reconcile_volume",
            },
            "version": 1,
        },
    )


def test_configure_all_override_installation(ws_installer, ws):
    prompts = MockPrompts(
        {
            r"Do you want to override the existing installation?": "yes",
            r"Select the source dialect": ALL_INSTALLED_DIALECTS.index("snowflake"),
            r"Select the transpiler": TRANSPILERS_FOR_SNOWFLAKE.index("Morpheus"),
            r"Enter input SQL path.*": "/tmp/queries/snow",
            r"Enter output directory.*": "/tmp/queries/databricks",
            r"Enter error file path.*": "/tmp/queries/errors.log",
            r"Would you like to validate.*": "no",
            r"Open .* in the browser?": "no",
            r"Select the Data Source": RECONCILE_DATA_SOURCES.index("snowflake"),
            r"Select the report type": RECONCILE_REPORT_TYPES.index("all"),
            r"Enter Secret scope name to store .* connection details / secrets": "remorph_snowflake",
            r"Enter source catalog name for .*": "snowflake_sample_data",
            r"Enter source schema name for .*": "tpch_sf1000",
            r"Enter target catalog name for Databricks": "tpch",
            r"Enter target schema name for Databricks": "1000gb",
        }
    )
    installation = MockInstallation(
        {
            "config.yml": {
                "transpiler_config_path": PATH_TO_TRANSPILER_CONFIG,
                "source_dialect": "snowflake",
                "catalog_name": "transpiler_test",
                "input_source": "sf_queries",
                "output_folder": "out_dir",
                "error_file_path": "error_log.log",
                "schema_name": "convertor_test",
                "sdk_config": {
                    "warehouse_id": "abc",
                },
                "version": 3,
            },
            "reconcile.yml": {
                "data_source": "snowflake",
                "report_type": "all",
                "secret_scope": "remorph_snowflake",
                "database_config": {
                    "source_catalog": "snowflake_sample_data",
                    "source_schema": "tpch_sf1000",
                    "target_catalog": "tpch",
                    "target_schema": "1000gb",
                },
                "metadata_config": {
                    "catalog": "remorph",
                    "schema": "reconcile",
                    "volume": "reconcile_volume",
                },
                "version": 1,
            },
        }
    )

    resource_configurator = create_autospec(ResourceConfigurator)
    resource_configurator.prompt_for_catalog_setup.return_value = "remorph"
    resource_configurator.prompt_for_schema_setup.return_value = "reconcile"
    resource_configurator.prompt_for_volume_setup.return_value = "reconcile_volume"

    ctx = ApplicationContext(ws)
    ctx.replace(
        prompts=prompts,
        installation=installation,
        resource_configurator=resource_configurator,
        workspace_installation=create_autospec(WorkspaceInstallation),
    )

    workspace_installer = ws_installer(
        ctx.workspace_client,
        ctx.prompts,
        ctx.installation,
        ctx.install_state,
        ctx.product_info,
        ctx.resource_configurator,
        ctx.workspace_installation,
    )

    config = workspace_installer.configure(module="all")

    expected_transpile_config = TranspileConfig(
        transpiler_config_path=PATH_TO_TRANSPILER_CONFIG,
        source_dialect="snowflake",
        input_source="/tmp/queries/snow",
        output_folder="/tmp/queries/databricks",
        error_file_path="/tmp/queries/errors.log",
        skip_validation=True,
        catalog_name="remorph",
        schema_name="transpiler",
    )

    expected_reconcile_config = ReconcileConfig(
        data_source="snowflake",
        report_type="all",
        secret_scope="remorph_snowflake",
        database_config=DatabaseConfig(
            source_schema="tpch_sf1000",
            target_catalog="tpch",
            target_schema="1000gb",
            source_catalog="snowflake_sample_data",
        ),
        metadata_config=ReconcileMetadataConfig(
            catalog="remorph",
            schema="reconcile",
            volume="reconcile_volume",
        ),
    )
    expected_config = RemorphConfigs(transpile=expected_transpile_config, reconcile=expected_reconcile_config)
    assert config == expected_config
    installation.assert_file_written(
        "config.yml",
        {
            "transpiler_config_path": PATH_TO_TRANSPILER_CONFIG,
            "catalog_name": "remorph",
            "input_source": "/tmp/queries/snow",
            "output_folder": "/tmp/queries/databricks",
            "error_file_path": "/tmp/queries/errors.log",
            "schema_name": "transpiler",
            "skip_validation": True,
            "source_dialect": "snowflake",
            "version": 3,
        },
    )

    installation.assert_file_written(
        "reconcile.yml",
        {
            "data_source": "snowflake",
            "report_type": "all",
            "secret_scope": "remorph_snowflake",
            "database_config": {
                "source_catalog": "snowflake_sample_data",
                "source_schema": "tpch_sf1000",
                "target_catalog": "tpch",
                "target_schema": "1000gb",
            },
            "metadata_config": {
                "catalog": "remorph",
                "schema": "reconcile",
                "volume": "reconcile_volume",
            },
            "version": 1,
        },
    )


def test_runs_upgrades_on_more_recent_version(ws_installer, ws):
    installation = MockInstallation(
        {
            'version.json': {'version': '0.3.0', 'wheel': '...', 'date': '...'},
            'state.json': {
                'resources': {
                    'dashboards': {'Reconciliation Metrics': 'abc'},
                    'jobs': {'Reconciliation Runner': '12345'},
                }
            },
            'config.yml': {
                "transpiler-config-path": PATH_TO_TRANSPILER_CONFIG,
                "source_dialect": "snowflake",
                "catalog_name": "upgrades",
                "input_source": "queries",
                "output_folder": "out",
                "error_file_path": "errors.log",
                "schema_name": "test",
                "sdk_config": {
                    "warehouse_id": "dummy",
                },
                "version": 3,
            },
        }
    )

    ctx = ApplicationContext(ws)
    prompts = MockPrompts(
        {
            r"Do you want to override the existing installation?": "yes",
            r"Select the source dialect": ALL_INSTALLED_DIALECTS.index("snowflake"),
            r"Select the transpiler": TRANSPILERS_FOR_SNOWFLAKE.index("Morpheus"),
            r"Enter input SQL path.*": "/tmp/queries/snow",
            r"Enter output directory.*": "/tmp/queries/databricks",
            r"Enter error file.*": "/tmp/queries/errors.log",
            r"Would you like to validate.*": "no",
            r"Open .* in the browser?": "no",
        }
    )
    wheels = create_autospec(WheelsV2)

    mock_workspace_installation = create_autospec(WorkspaceInstallation)

    ctx.replace(
        prompts=prompts,
        installation=installation,
        resource_configurator=create_autospec(ResourceConfigurator),
        workspace_installation=mock_workspace_installation,
        wheels=wheels,
    )

    workspace_installer = ws_installer(
        ctx.workspace_client,
        ctx.prompts,
        ctx.installation,
        ctx.install_state,
        ctx.product_info,
        ctx.resource_configurator,
        ctx.workspace_installation,
    )

    workspace_installer.run("transpile")

    mock_workspace_installation.install.assert_called_once_with(
        RemorphConfigs(
            transpile=TranspileConfig(
                transpiler_config_path=PATH_TO_TRANSPILER_CONFIG,
                source_dialect="snowflake",
                input_source="/tmp/queries/snow",
                output_folder="/tmp/queries/databricks",
                error_file_path="/tmp/queries/errors.log",
                catalog_name="remorph",
                schema_name="transpiler",
                skip_validation=True,
            )
        )
    )


def test_runs_and_stores_confirm_config_option(ws_installer, ws):
    prompts = MockPrompts(
        {
            r"Select the source dialect": ALL_INSTALLED_DIALECTS.index("snowflake"),
            r"Select the transpiler": TRANSPILERS_FOR_SNOWFLAKE.index("Remorph Community Transpiler"),
            r"Do you want to use the experimental Databricks generator ?": "yes",
            r"Enter input SQL path.*": "/tmp/queries/snow",
            r"Enter output directory.*": "/tmp/queries/databricks",
            r"Enter error file path.*": "/tmp/queries/errors.log",
            r"Would you like to validate.*": "yes",
            r"Do you want to use SQL Warehouse for validation?": "yes",
            r"Open .* in the browser?": "no",
        }
    )
    installation = MockInstallation()
    resource_configurator = create_autospec(ResourceConfigurator)
    resource_configurator.prompt_for_catalog_setup.return_value = "remorph_test"
    resource_configurator.prompt_for_schema_setup.return_value = "transpiler_test"
    resource_configurator.prompt_for_warehouse_setup.return_value = "w_id"

    ctx = ApplicationContext(ws)
    ctx.replace(
        prompts=prompts,
        installation=installation,
        resource_configurator=resource_configurator,
        workspace_installation=create_autospec(WorkspaceInstallation),
    )

    workspace_installer = ws_installer(
        ctx.workspace_client,
        ctx.prompts,
        ctx.installation,
        ctx.install_state,
        ctx.product_info,
        ctx.resource_configurator,
        ctx.workspace_installation,
    )

    TranspilerInstaller.transpilers_path = TranspilerInstaller.resources_folder

    config = workspace_installer.configure(module="transpile")

    expected_config = RemorphConfigs(
        transpile=TranspileConfig(
            transpiler_config_path=PATH_TO_TRANSPILER_CONFIG,
            transpiler_options={"-experimental": True},
            source_dialect="snowflake",
            input_source="/tmp/queries/snow",
            output_folder="/tmp/queries/databricks",
            error_file_path="/tmp/queries/errors.log",
            catalog_name="remorph_test",
            schema_name="transpiler_test",
            sdk_config={"warehouse_id": "w_id"},
        )
    )
    assert config == expected_config
    installation.assert_file_written(
        "config.yml",
        {
            "transpiler_config_path": PATH_TO_TRANSPILER_CONFIG,
            "transpiler_options": {'-experimental': True},
            "catalog_name": "remorph_test",
            "input_source": "/tmp/queries/snow",
            "output_folder": "/tmp/queries/databricks",
            "error_file_path": "/tmp/queries/errors.log",
            "schema_name": "transpiler_test",
            "sdk_config": {"warehouse_id": "w_id"},
            "source_dialect": "snowflake",
            "version": 3,
        },
    )


def test_runs_and_stores_force_config_option(ws_installer, ws):
    prompts = MockPrompts(
        {
            r"Select the source dialect": ALL_INSTALLED_DIALECTS.index("snowflake"),
            r"Select the transpiler": TRANSPILERS_FOR_SNOWFLAKE.index("Remorph Community Transpiler"),
            r"Enter input SQL path.*": "/tmp/queries/snow",
            r"Enter output directory.*": "/tmp/queries/databricks",
            r"Enter error file path.*": "/tmp/queries/errors.log",
            r"Would you like to validate.*": "yes",
            r"Do you want to use SQL Warehouse for validation?": "yes",
            r"Open .* in the browser?": "no",
        }
    )
    installation = MockInstallation()
    resource_configurator = create_autospec(ResourceConfigurator)
    resource_configurator.prompt_for_catalog_setup.return_value = "remorph_test"
    resource_configurator.prompt_for_schema_setup.return_value = "transpiler_test"
    resource_configurator.prompt_for_warehouse_setup.return_value = "w_id"

    ctx = ApplicationContext(ws)
    ctx.replace(
        prompts=prompts,
        installation=installation,
        resource_configurator=resource_configurator,
        workspace_installation=create_autospec(WorkspaceInstallation),
    )

    workspace_installer = ws_installer(
        ctx.workspace_client,
        ctx.prompts,
        ctx.installation,
        ctx.install_state,
        ctx.product_info,
        ctx.resource_configurator,
        ctx.workspace_installation,
    )

    TranspilerInstaller.transpiler_config_options = lambda a, b: [
        LSPConfigOptionV1(flag="-XX", method=LSPPromptMethod.FORCE, default=1254)
    ]

    config = workspace_installer.configure(module="transpile")

    expected_config = RemorphConfigs(
        transpile=TranspileConfig(
            transpiler_config_path=PATH_TO_TRANSPILER_CONFIG,
            transpiler_options={"-XX": 1254},
            source_dialect="snowflake",
            input_source="/tmp/queries/snow",
            output_folder="/tmp/queries/databricks",
            error_file_path="/tmp/queries/errors.log",
            catalog_name="remorph_test",
            schema_name="transpiler_test",
            sdk_config={"warehouse_id": "w_id"},
        )
    )
    assert config == expected_config
    installation.assert_file_written(
        "config.yml",
        {
            "transpiler_config_path": PATH_TO_TRANSPILER_CONFIG,
            "transpiler_options": {'-XX': 1254},
            "catalog_name": "remorph_test",
            "input_source": "/tmp/queries/snow",
            "output_folder": "/tmp/queries/databricks",
            "error_file_path": "/tmp/queries/errors.log",
            "schema_name": "transpiler_test",
            "sdk_config": {"warehouse_id": "w_id"},
            "source_dialect": "snowflake",
            "version": 3,
        },
    )


def test_runs_and_stores_question_config_option(ws_installer, ws):
    prompts = MockPrompts(
        {
            r"Select the source dialect": ALL_INSTALLED_DIALECTS.index("snowflake"),
            r"Select the transpiler": TRANSPILERS_FOR_SNOWFLAKE.index("Remorph Community Transpiler"),
            r"Max number of heaps:": 1254,
            r"Enter input SQL path.*": "/tmp/queries/snow",
            r"Enter output directory.*": "/tmp/queries/databricks",
            r"Enter error file path.*": "/tmp/queries/errors.log",
            r"Would you like to validate.*": "yes",
            r"Do you want to use SQL Warehouse for validation?": "yes",
            r"Open .* in the browser?": "no",
        }
    )
    installation = MockInstallation()
    resource_configurator = create_autospec(ResourceConfigurator)
    resource_configurator.prompt_for_catalog_setup.return_value = "remorph_test"
    resource_configurator.prompt_for_schema_setup.return_value = "transpiler_test"
    resource_configurator.prompt_for_warehouse_setup.return_value = "w_id"

    ctx = ApplicationContext(ws)
    ctx.replace(
        prompts=prompts,
        installation=installation,
        resource_configurator=resource_configurator,
        workspace_installation=create_autospec(WorkspaceInstallation),
    )

    workspace_installer = ws_installer(
        ctx.workspace_client,
        ctx.prompts,
        ctx.installation,
        ctx.install_state,
        ctx.product_info,
        ctx.resource_configurator,
        ctx.workspace_installation,
    )

    TranspilerInstaller.transpiler_config_options = lambda a, b: [
        LSPConfigOptionV1(flag="-XX", method=LSPPromptMethod.QUESTION, prompt="Max number of heaps:")
    ]

    config = workspace_installer.configure(module="transpile")

    expected_config = RemorphConfigs(
        transpile=TranspileConfig(
            transpiler_config_path=PATH_TO_TRANSPILER_CONFIG,
            transpiler_options={"-XX": 1254},
            source_dialect="snowflake",
            input_source="/tmp/queries/snow",
            output_folder="/tmp/queries/databricks",
            error_file_path="/tmp/queries/errors.log",
            catalog_name="remorph_test",
            schema_name="transpiler_test",
            sdk_config={"warehouse_id": "w_id"},
        )
    )
    assert config == expected_config
    installation.assert_file_written(
        "config.yml",
        {
            "transpiler_config_path": PATH_TO_TRANSPILER_CONFIG,
            "transpiler_options": {'-XX': 1254},
            "catalog_name": "remorph_test",
            "input_source": "/tmp/queries/snow",
            "output_folder": "/tmp/queries/databricks",
            "error_file_path": "/tmp/queries/errors.log",
            "schema_name": "transpiler_test",
            "sdk_config": {"warehouse_id": "w_id"},
            "source_dialect": "snowflake",
            "version": 3,
        },
    )


def test_runs_and_stores_choice_config_option(ws_installer, ws):
    prompts = MockPrompts(
        {
            r"Select the source dialect": ALL_INSTALLED_DIALECTS.index("snowflake"),
            r"Select the transpiler": TRANSPILERS_FOR_SNOWFLAKE.index("Remorph Community Transpiler"),
            r"Select currency:": 2,
            r"Enter input SQL path.*": "/tmp/queries/snow",
            r"Enter output directory.*": "/tmp/queries/databricks",
            r"Enter error file path.*": "/tmp/queries/errors.log",
            r"Would you like to validate.*": "yes",
            r"Do you want to use SQL Warehouse for validation?": "yes",
            r"Open .* in the browser?": "no",
        }
    )
    installation = MockInstallation()
    resource_configurator = create_autospec(ResourceConfigurator)
    resource_configurator.prompt_for_catalog_setup.return_value = "remorph_test"
    resource_configurator.prompt_for_schema_setup.return_value = "transpiler_test"
    resource_configurator.prompt_for_warehouse_setup.return_value = "w_id"

    ctx = ApplicationContext(ws)
    ctx.replace(
        prompts=prompts,
        installation=installation,
        resource_configurator=resource_configurator,
        workspace_installation=create_autospec(WorkspaceInstallation),
    )

    workspace_installer = ws_installer(
        ctx.workspace_client,
        ctx.prompts,
        ctx.installation,
        ctx.install_state,
        ctx.product_info,
        ctx.resource_configurator,
        ctx.workspace_installation,
    )

    TranspilerInstaller.transpiler_config_options = lambda a, b: [
        LSPConfigOptionV1(
            flag="-currency",
            method=LSPPromptMethod.CHOICE,
            prompt="Select currency:",
            choices=["CHF", "EUR", "GBP", "USD"],
        )
    ]

    config = workspace_installer.configure(module="transpile")

    expected_config = RemorphConfigs(
        transpile=TranspileConfig(
            transpiler_config_path=PATH_TO_TRANSPILER_CONFIG,
            transpiler_options={"-currency": "GBP"},
            source_dialect="snowflake",
            input_source="/tmp/queries/snow",
            output_folder="/tmp/queries/databricks",
            error_file_path="/tmp/queries/errors.log",
            catalog_name="remorph_test",
            schema_name="transpiler_test",
            sdk_config={"warehouse_id": "w_id"},
        )
    )
    assert config == expected_config
    installation.assert_file_written(
        "config.yml",
        {
            "transpiler_config_path": PATH_TO_TRANSPILER_CONFIG,
            "transpiler_options": {'-currency': "GBP"},
            "catalog_name": "remorph_test",
            "input_source": "/tmp/queries/snow",
            "output_folder": "/tmp/queries/databricks",
            "error_file_path": "/tmp/queries/errors.log",
            "schema_name": "transpiler_test",
            "sdk_config": {"warehouse_id": "w_id"},
            "source_dialect": "snowflake",
            "version": 3,
        },
    )
