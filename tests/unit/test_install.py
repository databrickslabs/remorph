from unittest.mock import create_autospec, patch

import pytest
from databricks.labs.blueprint.installation import MockInstallation
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import iam
from databricks.labs.blueprint.tui import MockPrompts
from databricks.labs.remorph.config import RemorphConfigs, ReconcileConfig, DatabaseConfig, ReconcileMetadataConfig
from databricks.labs.remorph.contexts.application import CliContext
from databricks.labs.remorph.deployment.configurator import ResourceConfigurator
from databricks.labs.remorph.deployment.installation import WorkspaceInstallation
from databricks.labs.remorph.install import WorkspaceInstaller, MODULES
from databricks.labs.remorph.config import MorphConfig
from databricks.labs.blueprint.wheels import ProductInfo
from databricks.labs.remorph.config import SQLGLOT_DIALECTS
from databricks.labs.remorph.reconcile.constants import SourceType, ReportType

RECONCILE_DATA_SOURCES = sorted([source_type.value for source_type in SourceType])
RECONCILE_REPORT_TYPES = sorted([report_type.value for report_type in ReportType])


@pytest.fixture
def ws():
    w = create_autospec(WorkspaceClient)
    w.current_user.me.side_effect = lambda: iam.User(
        user_name="me@example.com", groups=[iam.ComplexValue(display="admins")]
    )
    return w


def test_workspace_installer_run_raise_error_in_dbr(ws):
    ctx = CliContext(ws)
    resource_configurator = create_autospec(ResourceConfigurator)
    ws_installation = create_autospec(WorkspaceInstallation)
    environ = {"DATABRICKS_RUNTIME_VERSION": "8.3.x-scala2.12"}
    with pytest.raises(SystemExit):
        WorkspaceInstaller(ctx, resource_configurator, ws_installation, environ=environ)


def test_workspace_installer_run_install_not_called_in_test(ws):
    ctx = CliContext(ws)
    ctx.replace(product_info=ProductInfo.for_testing(RemorphConfigs))
    resource_configurator = create_autospec(ResourceConfigurator)
    ws_installation = create_autospec(WorkspaceInstallation)
    provided_config = RemorphConfigs()
    workspace_installer = WorkspaceInstaller(ctx, resource_configurator, ws_installation)
    returned_config = workspace_installer.run(config=provided_config)
    assert returned_config == provided_config
    ws_installation.install.assert_not_called()


def test_workspace_installer_run_install_called_with_provided_config(ws):
    ctx = CliContext(ws)
    resource_configurator = create_autospec(ResourceConfigurator)
    ws_installation = create_autospec(WorkspaceInstallation)
    provided_config = RemorphConfigs()
    workspace_installer = WorkspaceInstaller(ctx, resource_configurator, ws_installation)
    returned_config = workspace_installer.run(config=provided_config)
    assert returned_config == provided_config
    ws_installation.install.assert_called_once_with(provided_config)


def test_configure_error_if_invalid_module_selected(ws):
    ctx = CliContext(ws)
    resource_configurator = create_autospec(ResourceConfigurator)
    ws_installation = create_autospec(WorkspaceInstallation)
    workspace_installer = WorkspaceInstaller(ctx, resource_configurator, ws_installation)
    with pytest.raises(ValueError):
        workspace_installer.configure(module="invalid_module")


def test_workspace_installer_run_install_called_with_generated_config(ws):
    prompts = MockPrompts(
        {
            r"Select a module to configure:": MODULES.index("transpile"),
            r"Do you want to override the existing installation?": "no",
            r"Select the source": sorted(SQLGLOT_DIALECTS.keys()).index("snowflake"),
            r"Enter input SQL path.*": "/tmp/queries/snow",
            r"Enter output directory.*": "/tmp/queries/databricks",
            r"Would you like to validate.*": "no",
            r"Open .* in the browser?": "no",
        }
    )
    installation = MockInstallation()
    ctx = CliContext(ws)
    ctx.replace(prompts=prompts, installation=installation)
    resource_configurator = create_autospec(ResourceConfigurator)
    ws_installation = create_autospec(WorkspaceInstallation)
    workspace_installer = WorkspaceInstaller(ctx, resource_configurator, ws_installation)
    workspace_installer.run()
    installation.assert_file_written(
        "config.yml",
        {
            "catalog_name": "remorph",
            "input_sql": "/tmp/queries/snow",
            "mode": "current",
            "output_folder": "/tmp/queries/databricks",
            "schema_name": "transpiler",
            "skip_validation": True,
            "source": "snowflake",
            "version": 1,
        },
    )


def test_configure_transpile_no_existing_installation(ws):
    prompts = MockPrompts(
        {
            r"Select a module to configure:": MODULES.index("transpile"),
            r"Do you want to override the existing installation?": "no",
            r"Select the source": sorted(SQLGLOT_DIALECTS.keys()).index("snowflake"),
            r"Enter input SQL path.*": "/tmp/queries/snow",
            r"Enter output directory.*": "/tmp/queries/databricks",
            r"Would you like to validate.*": "no",
            r"Open .* in the browser?": "no",
        }
    )
    installation = MockInstallation()
    ctx = CliContext(ws)
    ctx.replace(prompts=prompts, installation=installation)
    resource_configurator = create_autospec(ResourceConfigurator)
    ws_installation = create_autospec(WorkspaceInstallation)
    workspace_installer = WorkspaceInstaller(ctx, resource_configurator, ws_installation)
    config = workspace_installer.configure()
    expected_morph_config = MorphConfig(
        source="snowflake",
        input_sql="/tmp/queries/snow",
        output_folder="/tmp/queries/databricks",
        skip_validation=True,
        catalog_name="remorph",
        schema_name="transpiler",
        mode="current",
    )
    expected_config = RemorphConfigs(morph=expected_morph_config)
    assert config == expected_config
    installation.assert_file_written(
        "config.yml",
        {
            "catalog_name": "remorph",
            "input_sql": "/tmp/queries/snow",
            "mode": "current",
            "output_folder": "/tmp/queries/databricks",
            "schema_name": "transpiler",
            "skip_validation": True,
            "source": "snowflake",
            "version": 1,
        },
    )


def test_configure_transpile_installation_no_override(ws):
    prompts = MockPrompts(
        {
            r"Select a module to configure:": MODULES.index("transpile"),
            r"Do you want to override the existing installation?": "no",
        }
    )
    ctx = CliContext(ws)
    ctx.replace(
        prompts=prompts,
        installation=MockInstallation(
            {
                "config.yml": {
                    "source": "snowflake",
                    "catalog_name": "transpiler_test",
                    "input_sql": "sf_queries",
                    "output_folder": "out_dir",
                    "schema_name": "convertor_test",
                    "sdk_config": {
                        "warehouse_id": "abc",
                    },
                    "version": 1,
                }
            }
        ),
    )
    resource_configurator = create_autospec(ResourceConfigurator)
    ws_installation = create_autospec(WorkspaceInstallation)
    workspace_installer = WorkspaceInstaller(ctx, resource_configurator, ws_installation)
    with pytest.raises(SystemExit):
        workspace_installer.configure()


def test_configure_transpile_installation_config_error_continue_install(ws):
    prompts = MockPrompts(
        {
            r"Select a module to configure:": MODULES.index("transpile"),
            r"Do you want to override the existing installation?": "no",
            r"Select the source": sorted(SQLGLOT_DIALECTS.keys()).index("snowflake"),
            r"Enter input SQL path.*": "/tmp/queries/snow",
            r"Enter output directory.*": "/tmp/queries/databricks",
            r"Would you like to validate.*": "no",
            r"Open .* in the browser?": "no",
        }
    )
    installation = MockInstallation(
        {
            "config.yml": {
                "source_name": "snowflake",  # Invalid key
                "catalog_name": "transpiler_test",
                "input_sql": "sf_queries",
                "output_folder": "out_dir",
                "schema_name": "convertor_test",
                "sdk_config": {
                    "warehouse_id": "abc",
                },
                "version": 1,
            }
        }
    )
    ctx = CliContext(ws)
    ctx.replace(
        prompts=prompts,
        installation=installation,
    )
    resource_configurator = create_autospec(ResourceConfigurator)
    ws_installation = create_autospec(WorkspaceInstallation)
    workspace_installer = WorkspaceInstaller(ctx, resource_configurator, ws_installation)
    config = workspace_installer.configure()
    expected_morph_config = MorphConfig(
        source="snowflake",
        input_sql="/tmp/queries/snow",
        output_folder="/tmp/queries/databricks",
        skip_validation=True,
        catalog_name="remorph",
        schema_name="transpiler",
        mode="current",
    )
    expected_config = RemorphConfigs(morph=expected_morph_config)
    assert config == expected_config
    installation.assert_file_written(
        "config.yml",
        {
            "catalog_name": "remorph",
            "input_sql": "/tmp/queries/snow",
            "mode": "current",
            "output_folder": "/tmp/queries/databricks",
            "schema_name": "transpiler",
            "skip_validation": True,
            "source": "snowflake",
            "version": 1,
        },
    )


@patch("webbrowser.open")
def test_configure_transpile_installation_with_no_validation(ws):
    prompts = MockPrompts(
        {
            r"Select a module to configure:": MODULES.index("transpile"),
            r"Select the source": sorted(SQLGLOT_DIALECTS.keys()).index("snowflake"),
            r"Enter input SQL path.*": "/tmp/queries/snow",
            r"Enter output directory.*": "/tmp/queries/databricks",
            r"Would you like to validate.*": "no",
            r"Open .* in the browser?": "yes",
        }
    )
    installation = MockInstallation()
    ctx = CliContext(ws)
    ctx.replace(
        prompts=prompts,
        installation=installation,
    )
    resource_configurator = create_autospec(ResourceConfigurator)
    ws_installation = create_autospec(WorkspaceInstallation)
    workspace_installer = WorkspaceInstaller(ctx, resource_configurator, ws_installation)
    config = workspace_installer.configure()
    expected_morph_config = MorphConfig(
        source="snowflake",
        input_sql="/tmp/queries/snow",
        output_folder="/tmp/queries/databricks",
        skip_validation=True,
        catalog_name="remorph",
        schema_name="transpiler",
        mode="current",
    )
    expected_config = RemorphConfigs(morph=expected_morph_config)
    assert config == expected_config
    installation.assert_file_written(
        "config.yml",
        {
            "catalog_name": "remorph",
            "input_sql": "/tmp/queries/snow",
            "mode": "current",
            "output_folder": "/tmp/queries/databricks",
            "schema_name": "transpiler",
            "skip_validation": True,
            "source": "snowflake",
            "version": 1,
        },
    )


def test_configure_transpile_installation_with_validation_and_cluster_id_in_config(ws):
    prompts = MockPrompts(
        {
            r"Select a module to configure:": MODULES.index("transpile"),
            r"Select the source": sorted(SQLGLOT_DIALECTS.keys()).index("snowflake"),
            r"Enter input SQL path.*": "/tmp/queries/snow",
            r"Enter output directory.*": "/tmp/queries/databricks",
            r"Would you like to validate.*": "yes",
            r"Do you want to use SQL Warehouse for validation?": "no",
            r"Open .* in the browser?": "no",
        }
    )
    installation = MockInstallation()
    ws.config.cluster_id = "1234"
    ctx = CliContext(ws)
    ctx.replace(
        prompts=prompts,
        installation=installation,
    )
    resource_configurator = create_autospec(ResourceConfigurator)
    resource_configurator.prompt_for_catalog_setup.return_value = "remorph_test"
    resource_configurator.prompt_for_schema_setup.return_value = "transpiler_test"
    ws_installation = create_autospec(WorkspaceInstallation)
    workspace_installer = WorkspaceInstaller(ctx, resource_configurator, ws_installation)
    config = workspace_installer.configure()
    expected_config = RemorphConfigs(
        morph=MorphConfig(
            source="snowflake",
            input_sql="/tmp/queries/snow",
            output_folder="/tmp/queries/databricks",
            catalog_name="remorph_test",
            schema_name="transpiler_test",
            mode="current",
            sdk_config={"cluster_id": "1234"},
        )
    )
    assert config == expected_config
    installation.assert_file_written(
        "config.yml",
        {
            "catalog_name": "remorph_test",
            "input_sql": "/tmp/queries/snow",
            "mode": "current",
            "output_folder": "/tmp/queries/databricks",
            "schema_name": "transpiler_test",
            "sdk_config": {"cluster_id": "1234"},
            "source": "snowflake",
            "version": 1,
        },
    )


def test_configure_transpile_installation_with_validation_and_cluster_id_from_prompt(ws):
    prompts = MockPrompts(
        {
            r"Select a module to configure:": MODULES.index("transpile"),
            r"Select the source": sorted(SQLGLOT_DIALECTS.keys()).index("snowflake"),
            r"Enter input SQL path.*": "/tmp/queries/snow",
            r"Enter output directory.*": "/tmp/queries/databricks",
            r"Would you like to validate.*": "yes",
            r"Do you want to use SQL Warehouse for validation?": "no",
            r"Enter a valid cluster_id to proceed": "1234",
            r"Open .* in the browser?": "no",
        }
    )
    installation = MockInstallation()
    ws.config.cluster_id = None
    ctx = CliContext(ws)
    ctx.replace(
        prompts=prompts,
        installation=installation,
    )
    resource_configurator = create_autospec(ResourceConfigurator)
    resource_configurator.prompt_for_catalog_setup.return_value = "remorph_test"
    resource_configurator.prompt_for_schema_setup.return_value = "transpiler_test"
    ws_installation = create_autospec(WorkspaceInstallation)
    workspace_installer = WorkspaceInstaller(ctx, resource_configurator, ws_installation)
    config = workspace_installer.configure()
    expected_config = RemorphConfigs(
        morph=MorphConfig(
            source="snowflake",
            input_sql="/tmp/queries/snow",
            output_folder="/tmp/queries/databricks",
            catalog_name="remorph_test",
            schema_name="transpiler_test",
            mode="current",
            sdk_config={"cluster_id": "1234"},
        )
    )
    assert config == expected_config
    installation.assert_file_written(
        "config.yml",
        {
            "catalog_name": "remorph_test",
            "input_sql": "/tmp/queries/snow",
            "mode": "current",
            "output_folder": "/tmp/queries/databricks",
            "schema_name": "transpiler_test",
            "sdk_config": {"cluster_id": "1234"},
            "source": "snowflake",
            "version": 1,
        },
    )


def test_configure_transpile_installation_with_validation_and_warehouse_id_from_prompt(ws):
    prompts = MockPrompts(
        {
            r"Select a module to configure:": MODULES.index("transpile"),
            r"Select the source": sorted(SQLGLOT_DIALECTS.keys()).index("snowflake"),
            r"Enter input SQL path.*": "/tmp/queries/snow",
            r"Enter output directory.*": "/tmp/queries/databricks",
            r"Would you like to validate.*": "yes",
            r"Do you want to use SQL Warehouse for validation?": "yes",
            r"Open .* in the browser?": "no",
        }
    )
    installation = MockInstallation()
    ctx = CliContext(ws)
    ctx.replace(
        prompts=prompts,
        installation=installation,
    )
    resource_configurator = create_autospec(ResourceConfigurator)
    resource_configurator.prompt_for_catalog_setup.return_value = "remorph_test"
    resource_configurator.prompt_for_schema_setup.return_value = "transpiler_test"
    resource_configurator.prompt_for_warehouse_setup.return_value = "w_id"
    ws_installation = create_autospec(WorkspaceInstallation)
    workspace_installer = WorkspaceInstaller(ctx, resource_configurator, ws_installation)
    config = workspace_installer.configure()
    expected_config = RemorphConfigs(
        morph=MorphConfig(
            source="snowflake",
            input_sql="/tmp/queries/snow",
            output_folder="/tmp/queries/databricks",
            catalog_name="remorph_test",
            schema_name="transpiler_test",
            mode="current",
            sdk_config={"warehouse_id": "w_id"},
        )
    )
    assert config == expected_config
    installation.assert_file_written(
        "config.yml",
        {
            "catalog_name": "remorph_test",
            "input_sql": "/tmp/queries/snow",
            "mode": "current",
            "output_folder": "/tmp/queries/databricks",
            "schema_name": "transpiler_test",
            "sdk_config": {"warehouse_id": "w_id"},
            "source": "snowflake",
            "version": 1,
        },
    )


def test_configure_reconcile_installation_no_override(ws):
    prompts = MockPrompts(
        {
            r"Select a module to configure:": MODULES.index("reconcile"),
            r"Do you want to override the existing installation?": "no",
        }
    )
    ctx = CliContext(ws)
    ctx.replace(
        prompts=prompts,
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
    resource_configurator = create_autospec(ResourceConfigurator)
    ws_installation = create_autospec(WorkspaceInstallation)
    workspace_installer = WorkspaceInstaller(ctx, resource_configurator, ws_installation)
    with pytest.raises(SystemExit):
        workspace_installer.configure()


def test_configure_reconcile_installation_config_error_continue_install(ws):
    prompts = MockPrompts(
        {
            r"Select a module to configure:": MODULES.index("reconcile"),
            r"Select the Data Source": RECONCILE_DATA_SOURCES.index("oracle"),
            r"Select the report type": RECONCILE_REPORT_TYPES.index("all"),
            r"Enter Secret scope name to store .* connection details / secrets": "remorph_oracle",
            r"Enter .* database name": "tpch_sf1000",
            r"Enter Databricks catalog name": "tpch",
            r"Enter Databricks schema name": "1000gb",
            r"Open .* in the browser?": "no",
        }
    )
    installation = MockInstallation(
        {
            "reconcile.yml": {
                "source": "oracle",  # Invalid key
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
    ctx = CliContext(ws)
    ctx.replace(
        prompts=prompts,
        installation=installation,
    )
    resource_configurator = create_autospec(ResourceConfigurator)
    resource_configurator.prompt_for_catalog_setup.return_value = "remorph"
    resource_configurator.prompt_for_schema_setup.return_value = "reconcile"
    resource_configurator.prompt_for_volume_setup.return_value = "reconcile_volume"
    ws_installation = create_autospec(WorkspaceInstallation)
    workspace_installer = WorkspaceInstaller(ctx, resource_configurator, ws_installation)
    config = workspace_installer.configure()
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
            r"Select a module to configure:": MODULES.index("reconcile"),
            r"Select the Data Source": RECONCILE_DATA_SOURCES.index("snowflake"),
            r"Select the report type": RECONCILE_REPORT_TYPES.index("all"),
            r"Enter Secret scope name to store .* connection details / secrets": "remorph_snowflake",
            r"Enter .* catalog name": "snowflake_sample_data",
            r"Enter .* schema name": "tpch_sf1000",
            r"Enter Databricks catalog name": "tpch",
            r"Enter Databricks schema name": "1000gb",
            r"Open .* in the browser?": "yes",
        }
    )
    installation = MockInstallation()
    ctx = CliContext(ws)
    ctx.replace(
        prompts=prompts,
        installation=installation,
    )
    resource_configurator = create_autospec(ResourceConfigurator)
    resource_configurator.prompt_for_catalog_setup.return_value = "remorph"
    resource_configurator.prompt_for_schema_setup.return_value = "reconcile"
    resource_configurator.prompt_for_volume_setup.return_value = "reconcile_volume"
    ws_installation = create_autospec(WorkspaceInstallation)
    workspace_installer = WorkspaceInstaller(ctx, resource_configurator, ws_installation)
    config = workspace_installer.configure()
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


def test_configure_all_override_installation(ws):
    prompts = MockPrompts(
        {
            r"Select a module to configure:": MODULES.index("all"),
            r"Do you want to override the existing installation?": "yes",
            r"Select the source": sorted(SQLGLOT_DIALECTS.keys()).index("snowflake"),
            r"Enter input SQL path.*": "/tmp/queries/snow",
            r"Enter output directory.*": "/tmp/queries/databricks",
            r"Would you like to validate.*": "no",
            r"Open .* in the browser?": "no",
            r"Select the Data Source": RECONCILE_DATA_SOURCES.index("snowflake"),
            r"Select the report type": RECONCILE_REPORT_TYPES.index("all"),
            r"Enter Secret scope name to store .* connection details / secrets": "remorph_snowflake",
            r"Enter .* catalog name": "snowflake_sample_data",
            r"Enter .* schema name": "tpch_sf1000",
            r"Enter Databricks catalog name": "tpch",
            r"Enter Databricks schema name": "1000gb",
        }
    )
    installation = MockInstallation(
        {
            "config.yml": {
                "source": "snowflake",
                "catalog_name": "transpiler_test",
                "input_sql": "sf_queries",
                "output_folder": "out_dir",
                "schema_name": "convertor_test",
                "sdk_config": {
                    "warehouse_id": "abc",
                },
                "version": 1,
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
    ctx = CliContext(ws)
    ctx.replace(
        prompts=prompts,
        installation=installation,
    )
    resource_configurator = create_autospec(ResourceConfigurator)
    resource_configurator.prompt_for_catalog_setup.return_value = "remorph"
    resource_configurator.prompt_for_schema_setup.return_value = "reconcile"
    resource_configurator.prompt_for_volume_setup.return_value = "reconcile_volume"
    ws_installation = create_autospec(WorkspaceInstallation)
    workspace_installer = WorkspaceInstaller(ctx, resource_configurator, ws_installation)
    config = workspace_installer.configure()
    expected_morph_config = MorphConfig(
        source="snowflake",
        input_sql="/tmp/queries/snow",
        output_folder="/tmp/queries/databricks",
        skip_validation=True,
        catalog_name="remorph",
        schema_name="transpiler",
        mode="current",
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
    expected_config = RemorphConfigs(morph=expected_morph_config, reconcile=expected_reconcile_config)
    assert config == expected_config
    installation.assert_file_written(
        "config.yml",
        {
            "catalog_name": "remorph",
            "input_sql": "/tmp/queries/snow",
            "mode": "current",
            "output_folder": "/tmp/queries/databricks",
            "schema_name": "transpiler",
            "skip_validation": True,
            "source": "snowflake",
            "version": 1,
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
