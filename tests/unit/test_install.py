import webbrowser
from datetime import timedelta
from unittest import mock
from unittest.mock import create_autospec, patch

import pytest

from databricks.labs.remorph.helpers.dashboard_publisher import DashboardPublisher

from databricks.labs.blueprint.installation import Installation, MockInstallation
from databricks.labs.blueprint.tui import MockPrompts, Prompts
from databricks.labs.lsql.backends import MockBackend
from databricks.labs.remorph.config import (
    MorphConfig,
    RemorphConfigs,
    ReconcileConfig,
    DatabaseConfig,
    ReconcileMetadataConfig,
)
from databricks.labs.remorph.helpers.deployment import TableDeployer, JobDeployer
from databricks.labs.remorph.install import (
    CatalogSetup,
    WorkspaceInstallation,
    WorkspaceInstaller,
    ReconciliationMetadataSetup,
)
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import NotFound
from databricks.sdk.service.catalog import CatalogInfo, SchemaInfo, VolumeInfo
from databricks.labs.blueprint.wheels import ProductInfo
from databricks.sdk.service.compute import State
from databricks.sdk.service.sql import (
    DataSource,
    EndpointInfo,
    EndpointInfoWarehouseType,
)
from databricks.labs.blueprint.parallel import ManyError

MODULES = ["all", "reconcile", "transpile"]

SOURCES = [
    "athena",
    "bigquery",
    "databricks",
    "experimental",
    "mysql",
    "netezza",
    "oracle",
    "postgresql",
    "presto",
    "redshift",
    "snowflake",
    "sqlite",
    "teradata",
    "trino",
    "tsql",
    "vertica",
]


@pytest.fixture
def ws():
    w = create_autospec(WorkspaceClient)
    w.config.host = "https://foo"
    w.config.return_value = {"warehouse_id", "test_warehouse"}
    w.data_sources.list = lambda: [DataSource(id="bcd", warehouse_id="abc")]
    w.warehouses.list = lambda **_: [
        EndpointInfo(name="abc", id="abc", warehouse_type=EndpointInfoWarehouseType.PRO, state=State.RUNNING)
    ]
    return w


@pytest.fixture
def ws_no_catalog_schema():
    w = create_autospec(WorkspaceClient)
    w.catalogs.get.side_effect = NotFound("test")
    w.schemas.get.side_effect = NotFound("test.schema")
    w.catalogs.create.return_value = CatalogInfo.from_dict({"name": "test"})
    w.schemas.create.return_value = SchemaInfo.from_dict({"name": "schema", "catalog_name": "test"})
    return w


@pytest.fixture
def mock_installation():
    return MockInstallation(
        {
            "config.yml": {
                "source": "snowflake",
                "catalog_name": "transpiler_test",
                "input_sql": "sf_queries",
                "mode": "current",
                "output_folder": "out_dir",
                "skip_validation": False,
                "schema_name": "convertor_test",
                "sdk_config": {
                    "warehouse_id": "abc",
                },
                "version": 1,
            },
            "reconcile.yml": {
                "data_source": "snowflake",
                "database_config": {
                    "source_catalog": "snowflake_sample_data",
                    "source_schema": "tpch_sf1000",
                    "target_catalog": "tpch",
                    "target_schema": "1000gb",
                },
                "report_type": "all",
                "secret_scope": "remorph_snowflake",
                "tables": {
                    "filter_type": "exclude",
                    "tables_list": ["SUPPLIER", "FRIENDS", "ORDERS", "PART"],
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


@pytest.fixture
def mock_installation_state():
    return MockInstallation(
        {
            "state.json": {
                "source": "dummy",
            }
        }
    )


@patch("webbrowser.open")
def test_install(ws, mock_installation_state):
    prompts = MockPrompts(
        {
            r"Select a module to configure:": MODULES.index("all"),
            r"Select the source": SOURCES.index("bigquery"),
            r"Enter Input SQL path.*": "data/queries/bigquery",
            r"Enter Output directory.*": "transpiled",
            r"Would you like to validate the Syntax, Semantics of the transpiled queries?": "no",
            r"Open .* in the browser and continue...?": "yes",
            r"Select the Data Source:": 2,
            r"Select the Report Type:": 0,
            r"Enter Secret Scope name to store .* connection details / secrets": "remorph_snowflake",
            r"Enter .* Catalog name": "snowflake_sample_data",
            r"Enter .* Database name": "tpch_sf1000",
            r"Enter Databricks Catalog name": "tpch",
            r"Enter Databricks Schema name": "1000gb",
            r"Enter Catalog name to store reconcile metadata": "remorph",
            r"Enter Schema name to store reconcile metadata": "reconcile",
        }
    )
    install = WorkspaceInstaller(ws, mock_installation_state, prompts=prompts)

    # Assert that the `install` is an instance of WorkspaceInstaller
    assert isinstance(install, WorkspaceInstaller)

    with patch.object(WorkspaceInstallation, "run", autospec=True):
        configs = install.run()
        config = configs.morph
        reconcile_config = configs.reconcile

        assert config.source == "bigquery"
        assert config.sdk_config is None
        assert config.input_sql == "data/queries/bigquery"
        assert config.output_folder == "transpiled"
        assert config.skip_validation is True
        assert config.catalog_name == "transpiler_test"
        assert config.schema_name == "convertor_test"
        assert config.mode == "current"

        assert reconcile_config.data_source == "snowflake"
        assert reconcile_config.database_config.source_catalog == "snowflake_sample_data"
        assert reconcile_config.database_config.source_schema == "tpch_sf1000"
        assert reconcile_config.database_config.target_catalog == "tpch"
        assert reconcile_config.database_config.target_schema == "1000gb"
        assert reconcile_config.report_type == "all"
        assert reconcile_config.secret_scope == "remorph_snowflake"
        assert reconcile_config.tables is None


def test_install_dbr(ws, mock_installation, monkeypatch):
    monkeypatch.setenv("DATABRICKS_RUNTIME_VERSION", "14.1")

    with pytest.raises(SystemExit):
        install = WorkspaceInstaller(ws, MockPrompts({}))
        install.run()


def test_save_config(ws, mock_installation, monkeypatch):
    def mock_open(url):
        print(f"Opening URL: {url}")

    monkeypatch.setattr("webbrowser.open", mock_open)
    prompts = MockPrompts(
        {
            r"Select a module to configure:": MODULES.index("transpile"),
            r"Select the source": SOURCES.index("snowflake"),
            r"Enter Input SQL path.*": "sf_queries",
            r"Enter Output directory.*": "out_dir",
            r"Would you like to validate the Syntax, Semantics of the transpiled queries?": "yes",
            r"Do you want to use SQL Warehouse for validation?": "yes",
            r".*PRO or SERVERLESS SQL warehouse.*": "1",
            r"Enter Catalog for Validation": "transpiler_test",
            r"Enter Schema for Validation": "convertor_test",
            r"Open .* in the browser and continue...?": "yes",
        }
    )
    install = WorkspaceInstaller(ws, mock_installation, prompts)
    webbrowser.open('https://localhost/#workspace~/mock/config.yml')
    install.configure()

    mock_installation.assert_file_written(
        "config.yml",
        {
            "source": "snowflake",
            "sdk_config": {
                "warehouse_id": "abc",
            },
            "input_sql": "sf_queries",
            "output_folder": "out_dir",
            "skip_validation": False,
            "catalog_name": "transpiler_test",
            "schema_name": "convertor_test",
            "mode": "current",
        },
    )


def test_create_sql_warehouse(ws_no_catalog_schema, mock_installation_state):
    ws_client = ws_no_catalog_schema

    prompts = MockPrompts(
        {
            r"Select a module to configure:": MODULES.index("transpile"),
            r"Select the source": SOURCES.index("snowflake"),
            r"Enter Input SQL path.*": "sf_queries",
            r"Enter Output directory.*": "out_dir",
            r"Would you like to validate the Syntax, Semantics of the transpiled queries?": "yes",
            r"Do you want to use SQL Warehouse for validation?": "yes",
            r"Select PRO or SERVERLESS SQL warehouse to run validation on": "0",
            r"Enter Catalog for Validation": "test",
            r".*Do you want to create a new one?": "yes",
            r"Enter Schema for Validation": "schema",
            r".*Do you want to create a new Schema?": "yes",
            r"Open .* in the browser and continue...?": "no",
        }
    )

    install = WorkspaceInstaller(ws_client, mock_installation_state, prompts)

    # Assert that the `install` is an instance of WorkspaceInstaller
    assert isinstance(install, WorkspaceInstaller)

    configs = install.configure()

    config = configs.morph

    # Assert that the `config` is an instance of MorphConfig
    assert isinstance(config, MorphConfig)

    # Assert  the `config` variables
    assert config.source == "snowflake"
    assert config.skip_validation is False
    assert config.catalog_name == "test"
    assert config.schema_name == "schema"


def test_get_cluster_id(ws, mock_installation_state):
    prompts = MockPrompts(
        {
            r"Select a module to configure:": MODULES.index("transpile"),
            r"Select the source": SOURCES.index("snowflake"),
            r"Enter Input SQL path.*": "sf_queries",
            r"Enter Output directory.*": "out_dir",
            r"Would you like to validate the Syntax, Semantics of the transpiled queries?": "yes",
            r"Do you want to use SQL Warehouse for validation?": "no",
            r"Enter a valid cluster_id to proceed": "test_cluster",
            r"Enter Catalog for Validation": "test",
            r".*Do you want to create a new one?": "yes",
            r"Enter Schema for Validation": "schema",
            r".*Do you want to create a new Schema?": "yes",
            r"Open .* in the browser and continue...?": "no",
        }
    )
    ws.config.cluster_id = None  # setting this to None when cluster_id is not set in default configuration.

    install = WorkspaceInstaller(ws, mock_installation_state, prompts)

    # Assert that the `install` is an instance of WorkspaceInstaller
    assert isinstance(install, WorkspaceInstaller)

    configs = install.configure()

    config = configs.morph
    # Assert that the `config` is an instance of MorphConfig
    assert isinstance(config, MorphConfig)

    # Assert  the `config` variables
    assert config.source == "snowflake"
    assert config.skip_validation is False
    assert config.catalog_name == "test"
    assert config.schema_name == "schema"
    assert config.sdk_config.get("cluster_id") == "test_cluster"


def test_create_catalog_no(ws_no_catalog_schema, mock_installation_state):
    prompts = MockPrompts(
        {
            r"Select a module to configure:": MODULES.index("transpile"),
            r"Select the source": SOURCES.index("snowflake"),
            r"Enter Input SQL path.*": "sf_queries",
            r"Enter Output directory.*": "out_dir",
            r"Would you like to validate the Syntax, Semantics of the transpiled queries?": "yes",
            r"Do you want to use SQL Warehouse for validation?": "no",
            r"Enter a valid cluster_id to proceed": "test_cluster",
            r"Enter Catalog for Validation": "test",
            r".*Do you want to create a new one?": "no",
        }
    )
    install = WorkspaceInstaller(ws_no_catalog_schema, mock_installation_state, prompts)

    with pytest.raises(SystemExit):
        install.configure()


def test_create_schema_no(ws_no_catalog_schema, mock_installation_state):
    prompts = MockPrompts(
        {
            r"Select a module to configure:": MODULES.index("transpile"),
            r"Select the source": SOURCES.index("snowflake"),
            r"Enter Input SQL path.*": "sf_queries",
            r"Enter Output directory.*": "out_dir",
            r"Would you like to validate the Syntax, Semantics of the transpiled queries?": "yes",
            r"Do you want to use SQL Warehouse for validation?": "no",
            r"Enter a valid cluster_id to proceed": "test_cluster",
            r"Enter Catalog for Validation": "test",
            r".*Do you want to create a new one?": "yes",
            r"Enter schema_name": "schema",
            r".*Do you want to create a new Schema?": "no",
            r".*": "",
        }
    )
    install = WorkspaceInstaller(ws_no_catalog_schema, mock_installation_state, prompts)

    with pytest.raises(SystemExit):
        install.configure()


def test_workspace_installation(ws, mock_installation, monkeypatch):
    # Create a mock for the Installation
    mock_install = create_autospec(Installation)

    # Create a mock for the config
    config = create_autospec(MorphConfig)

    product_info = create_autospec(ProductInfo)

    # Call the current function
    result = WorkspaceInstallation(config, mock_install, ws, Prompts(), timedelta(minutes=2), product_info)

    # Assert that the result is an instance of WorkspaceInstallation
    assert isinstance(result, WorkspaceInstallation)


def test_get_catalog():
    mock_ws = create_autospec(WorkspaceClient)
    mock_ws.catalogs.get.return_value = CatalogInfo.from_dict({"name": "test_catalog"})

    # Create a mock for the Catalog Setup
    catalog_setup = CatalogSetup(mock_ws)

    assert catalog_setup.get("test_catalog") == "test_catalog"


def test_get_schema(ws):
    mock_ws = create_autospec(WorkspaceClient)
    mock_ws.schemas.get.return_value = SchemaInfo.from_dict({"name": "test.schema"})

    # Create a mock for the Catalog Setup
    catalog_setup = CatalogSetup(mock_ws)

    assert catalog_setup.get_schema("test.schema") == "test.schema"


def test_config(ws):
    config = MorphConfig(
        source="snowflake",
        skip_validation=False,
        catalog_name="test_catalog",
        schema_name="test_schema",
        sdk_config=None,
    )
    assert isinstance(config, MorphConfig)


def test_save_reconcile_config(ws, mock_installation, monkeypatch):
    def mock_open(url):
        print(f"Opening URL: {url}")

    monkeypatch.setattr("webbrowser.open", mock_open)
    prompts = MockPrompts(
        {
            r"Select a module to configure:": MODULES.index("reconcile"),
            r"Select the Data Source:": 2,
            r"Select the Report Type:": 0,
            r"Enter Secret Scope name to store .* connection details / secrets": "remorph_snowflake",
            r"Enter .* Catalog name": "snowflake_sample_data",
            r"Enter .* Database name": "tpch_sf1000",
            r"Enter Databricks Catalog name": "tpch",
            r"Enter Databricks Schema name": "1000gb",
            r"Enter Catalog name to store reconcile metadata": "remorph",
            r"Enter Schema name to store reconcile metadata": "reconcile",
            r"Open .* in the browser and continue...?": "yes",
        }
    )
    install = WorkspaceInstaller(ws, mock_installation, prompts)

    webbrowser.open('https://localhost/#workspace~/mock/config.yml')
    install.configure()

    mock_installation.assert_file_written(
        "reconcile.yml",
        {
            "data_source": "snowflake",
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
            "report_type": "all",
            "secret_scope": "remorph_snowflake",
            "tables": {
                "filter_type": "exclude",
                "tables_list": ["SUPPLIER", "FRIENDS", "ORDERS", "PART"],
            },
        },
    )


def test_workspace_installation_run(ws, mock_installation_state, monkeypatch):
    def mock_open(url):
        print(f"Opening URL: {url}")

    monkeypatch.setattr("webbrowser.open", mock_open)
    prompts = MockPrompts(
        {
            r"Select a module to configure:": MODULES.index("reconcile"),
            r"Select the Data Source:": 2,
            r"Select the Report Type:": 0,
            r"Enter Secret Scope name to store .* connection details / secrets": "remorph_snowflake",
            r"Enter .* Catalog name": "snowflake_sample_data",
            r"Enter .* Database name": "tpch_sf1000",
            r"Enter Databricks Catalog name": "tpch",
            r"Enter Databricks Schema name": "1000gb",
            r"Enter Catalog name to store reconcile metadata": "remorph",
            r"Enter Schema name to store reconcile metadata": "reconcile",
            r"Open .* in the browser and continue...?": "yes",
        }
    )
    install = WorkspaceInstaller(ws, mock_installation_state, prompts)

    webbrowser.open('https://localhost/#workspace~/mock/config.yml')

    with patch.object(WorkspaceInstallation, "run", return_value=None) as mock_run:
        mock_run.side_effect = ManyError([NotFound("test1"), NotFound("test2")])
        with pytest.raises(ManyError):
            install.run()


def test_workspace_installation_run_single_error(ws, monkeypatch):

    mock_installation_reconcile = MockInstallation(
        {
            "reconcile.yml": {
                "config": {
                    "source_catalog": "snowflake_sample_data",
                    "source_schema": "tpch_sf1000",
                    "target_catalog": "tpch",
                    "target_schema": "1000gb",
                },
                "report_type": "all",
                "secret_scope": "remorph_snowflake",
                "tables": {
                    "filter_type": "exclude",
                    "tables_list": ["SUPPLIER", "FRIENDS", "ORDERS", "PART"],
                },
                "version": 1,
            }
        }
    )

    def mock_open(url):
        print(f"Opening URL: {url}")

    monkeypatch.setattr("webbrowser.open", mock_open)
    prompts = MockPrompts(
        {
            r"Select a module to configure:": MODULES.index("reconcile"),
            r"Select the Data Source:": 2,
            r"Select the Report Type:": 0,
            r"Enter Secret Scope name to store .* connection details / secrets": "remorph_snowflake",
            r"Enter .* Catalog name": "snowflake_sample_data",
            r"Enter .* Database name": "tpch_sf1000",
            r"Enter Databricks Catalog name": "tpch",
            r"Enter Databricks Schema name": "1000gb",
            r"Enter Catalog name to store reconcile metadata": "remorph",
            r"Enter Schema name to store reconcile metadata": "reconcile",
            r"Open .* in the browser and continue...?": "yes",
        }
    )
    install = WorkspaceInstaller(ws, mock_installation_reconcile, prompts)

    webbrowser.open('https://localhost/#workspace~/mock/config.yml')

    with patch.object(WorkspaceInstallation, "run", return_value=None) as mock_run:
        mock_run.side_effect = ManyError([NotFound("test1")])
        with pytest.raises(NotFound):
            install.run()


def test_morph_config_error(ws, monkeypatch):
    mock_installation_config = MockInstallation(
        {
            "config.yml": {
                "catalog_name": "transpiler_test",
                "input_sql": "sf_queries",
                "mode": "current",
                "output_folder": "out_dir",
                "skip_validation": False,
                "schema_name": "convertor_test",
                "sdk_config": {
                    "warehouse_id": "abc",
                },
                "version": 1,
            }
        }
    )

    def mock_open(url):
        print(f"Opening URL: {url}")

    monkeypatch.setattr("webbrowser.open", mock_open)

    prompts = MockPrompts(
        {
            r"Select a module to configure:": MODULES.index("transpile"),
            r"Select the source": SOURCES.index("snowflake"),
            r"Enter Input SQL path.*": "sf_queries",
            r"Enter Output directory.*": "out_dir",
            r"Would you like to validate the Syntax, Semantics of the transpiled queries?": "yes",
            r"Do you want to use SQL Warehouse for validation?": "no",
            r"Enter a valid cluster_id to proceed": "test_cluster",
            r"Enter Catalog for Validation": "test",
            r".*Do you want to create a new one?": "yes",
            r"Enter schema_name": "schema",
            r".*Do you want to create a new Schema?": "no",
            r".*": "",
        }
    )

    install = WorkspaceInstaller(ws, mock_installation_config, prompts)
    webbrowser.open('https://localhost/#workspace~/mock/config.yml')
    install.configure()


def test_recon_metadata_setup(ws):
    recon_config = ReconcileConfig(
        data_source="snowflake",
        report_type="all",
        secret_scope="remorph_snowflake",
        database_config=DatabaseConfig(
            source_catalog="snowflake_sample_data",
            source_schema="tpch_sf1000",
            target_catalog="tpch",
            target_schema="1000gb",
        ),
        metadata_config=ReconcileMetadataConfig(catalog="remorph", schema="reconcile"),
        job_id="123",
        tables=None,
    )

    catalog_setup = create_autospec(CatalogSetup)
    sql_backend = MockBackend()
    table_deployer = TableDeployer(sql_backend, "remorph", "reconcile")

    recon_metadata_setup = ReconciliationMetadataSetup(ws, recon_config, catalog_setup, table_deployer)
    recon_metadata_setup.configure_catalog()
    catalog_setup.get.assert_called_with("remorph")

    recon_metadata_setup.configure_schema()
    catalog_setup.get_schema.assert_called_with("remorph.reconcile")

    catalog_setup.get.side_effect = NotFound("Not found")
    recon_metadata_setup.configure_catalog()
    catalog_setup.create.assert_called_with("remorph")

    catalog_setup.get_schema.side_effect = NotFound("Not found")
    recon_metadata_setup.configure_schema()
    catalog_setup.create_schema.assert_called_with("reconcile", "remorph")

    recon_metadata_setup.deploy_tables()
    assert len(sql_backend.queries) > 0


@mock.patch.object(DashboardPublisher, 'create', autospec=True)
@mock.patch.object(ReconciliationMetadataSetup, 'run', autospec=True)
@mock.patch.object(JobDeployer, 'deploy_job', autospec=True)
def test_recon_workspace_installation(deploy_job, metadata_setup_run, create_dashboard, ws):
    installation = MockInstallation(is_global=False)
    product_info = ProductInfo.from_class(ReconcileConfig)
    prompts = MockPrompts({})
    remorph_configs = RemorphConfigs(
        morph=None,
        reconcile=ReconcileConfig(
            data_source="snowflake",
            report_type="all",
            secret_scope="remorph_snowflake",
            database_config=DatabaseConfig(
                source_catalog="snowflake_sample_data",
                source_schema="tpch_sf1000",
                target_catalog="tpch",
                target_schema="1000gb",
            ),
            metadata_config=ReconcileMetadataConfig(catalog="remorph", schema="reconcile"),
            job_id="123",
            tables=None,
        ),
    )

    workspace_installation = WorkspaceInstallation(
        remorph_configs,
        installation,
        ws,
        prompts,
        timedelta(minutes=2),
        product_info,
    )

    with patch("databricks.labs.remorph.helpers.db_sql.get_sql_backend", return_value=MockBackend()):
        workspace_installation.run()

    ws.volumes.create.assert_called_once()
    create_dashboard.assert_called_once()
    metadata_setup_run.assert_called_once()
    deploy_job.assert_called_once()


def test_recon_workspace_installation_with_existing_volume(ws):
    installation = MockInstallation(is_global=False)
    product_info = ProductInfo.from_class(ReconcileConfig)
    prompts = MockPrompts({})
    remorph_configs = RemorphConfigs(
        morph=None,
        reconcile=ReconcileConfig(
            data_source="snowflake",
            report_type="all",
            secret_scope="remorph_snowflake",
            database_config=DatabaseConfig(
                source_catalog="snowflake_sample_data",
                source_schema="tpch_sf1000",
                target_catalog="tpch",
                target_schema="1000gb",
            ),
            metadata_config=ReconcileMetadataConfig(catalog="remorph", schema="reconcile"),
            job_id="123",
            tables=None,
        ),
    )

    workspace_installation = WorkspaceInstallation(
        remorph_configs,
        installation,
        ws,
        prompts,
        timedelta(minutes=2),
        product_info,
    )

    ws.volumes.list.return_value = [
        VolumeInfo(volume_id="122", name="volume1"),
        VolumeInfo(volume_id="123", name="reconcile_volume"),
    ]

    with patch("databricks.labs.remorph.helpers.db_sql.get_sql_backend", return_value=MockBackend()):
        workspace_installation.run()

    ws.volumes.create.assert_not_called()
