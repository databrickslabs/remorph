import webbrowser
from datetime import timedelta
from unittest.mock import create_autospec

import pytest
from databricks.labs.blueprint.installation import Installation, MockInstallation
from databricks.labs.blueprint.tui import MockPrompts, Prompts
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import NotFound
from databricks.sdk.service.catalog import CatalogInfo

from databricks.labs.remorph.config import MorphConfig
from databricks.labs.remorph.install import (
    CatalogSetup,
    WorkspaceInstallation,
    WorkspaceInstaller,
)


@pytest.fixture
def ws():
    w = create_autospec(WorkspaceClient)
    w.catalogs.get.side_effect = NotFound("test")
    w.schemas.get.side_effect = NotFound("test.schema")
    return w


@pytest.fixture
def mock_installation():
    return MockInstallation(
        {"state.json": {"version": 1, "source": "snowflake", "skip_validation": True, "catalog_name": "remorph_test"}}
    )


def test_install(ws, mock_installation):
    prompts = MockPrompts(
        {
            r"Select the source": "0",
            r"Do you want to Skip Validation": "yes",
            r"Enter catalog_name": "remorph_test",
            r".*Do you want to create a new one?": "yes",
            r"Enter schema_name": "remorph_schema",
            r".*Do you want to create a new Schema?": "yes",
            r".*": "",
        }
    )
    install = WorkspaceInstaller(prompts, mock_installation, ws)

    # Assert that the `install` is an instance of WorkspaceInstaller
    assert isinstance(install, WorkspaceInstaller)

    install.run()


def test_install_dbr(ws, mock_installation, monkeypatch):
    monkeypatch.setenv("DATABRICKS_RUNTIME_VERSION", "14.1")
    prompts = MockPrompts(
        {
            r"Select the source": "0",
            r"Do you want to Skip Validation": "yes",
            r".*": "",
        }
    )
    with pytest.raises(SystemExit):
        install = WorkspaceInstaller(prompts, mock_installation, ws)
        install.run()


def test_save_config(ws, mock_installation):
    prompts = MockPrompts(
        {
            r"Select the source": "0",
            r"Do you want to Skip Validation": "yes",
            r"Enter catalog_name": "remorph_catalog",
            r".*Do you want to create a new one?": "yes",
            r"Enter schema_name": "remorph_schema",
            r".*Do you want to create a new Schema?": "yes",
            r"Open config file in the browser.*": "yes",
            r".*": "",
        }
    )
    install = WorkspaceInstaller(prompts, mock_installation, ws)
    webbrowser.open = lambda x: x
    install.configure()

    mock_installation.assert_file_written(
        "config.yml",
        {
            "version": 1,
            "source": "snowflake",
            "skip_validation": True,
            "catalog_name": "remorph_catalog",
            "schema_name": "remorph_schema",
        },
    )


def test_create_catalog_schema(ws, mock_installation):
    prompts = MockPrompts(
        {
            r"Select the source": "0",
            r"Do you want to Skip Validation": "yes",
            r"Enter catalog_name": "test",
            r".*Do you want to create a new one?": "yes",
            r"Enter schema_name": "schema",
            r".*Do you want to create a new Schema?": "yes",
            r".*": "",
        }
    )
    install = WorkspaceInstaller(prompts, mock_installation, ws)

    # Assert that the `install` is an instance of WorkspaceInstaller
    assert isinstance(install, WorkspaceInstaller)

    config = install.configure()

    # Assert that the `config` is an instance of MorphConfig
    assert isinstance(config, MorphConfig)

    # Assert  the `config` variables
    assert config.source == "snowflake"
    assert config.skip_validation is True
    assert config.catalog_name == "test"
    assert config.schema_name == "schema"


def test_create_catalog_no(ws, mock_installation):
    prompts = MockPrompts(
        {
            r"Select the source": "0",
            r"Do you want to Skip Validation": "yes",
            r"Enter catalog_name": "test",
            r".*Do you want to create a new one?": "no",
            r".*": "",
        }
    )
    install = WorkspaceInstaller(prompts, mock_installation, ws)
    with pytest.raises(SystemExit):
        install.configure()


def test_create_schema_no(ws, mock_installation):
    prompts = MockPrompts(
        {
            r"Select the source": "0",
            r"Do you want to Skip Validation": "yes",
            r"Enter catalog_name": "test",
            r".*Do you want to create a new one?": "yes",
            r"Enter schema_name": "schema",
            r".*Do you want to create a new Schema?": "no",
            r".*": "",
        }
    )
    install = WorkspaceInstaller(prompts, mock_installation, ws)
    with pytest.raises(SystemExit):
        install.configure()


def test_workspace_installation(ws, mock_installation, monkeypatch):
    # Create a mock for the Installation
    mock_install = create_autospec(Installation)

    # Create a mock for the config
    config = create_autospec(MorphConfig)

    # Call the current function
    result = WorkspaceInstallation(config, mock_install, ws, Prompts(), timedelta(minutes=2))

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
    mock_ws.schemas.get.return_value = CatalogInfo.from_dict({"name": "test.schema"})

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
