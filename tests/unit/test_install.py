import webbrowser
from unittest.mock import MagicMock, create_autospec

import pytest
from databricks.labs.blueprint.installation import Installation, MockInstallation
from databricks.labs.blueprint.tui import MockPrompts
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import NotFound

from databricks.labs.remorph.__about__ import __version__
from databricks.labs.remorph.install import WorkspaceInstallation, WorkspaceInstaller


@pytest.fixture
def ws():
    ws = create_autospec(WorkspaceClient)

    ws.product = "remorph"
    ws.product_version = __version__

    return ws


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
            r"Enter schema_name": "remorph_schema",
            r".*": "",
        }
    )
    install = WorkspaceInstaller(prompts, mock_installation, ws)
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
            r"Enter schema_name": "remorph_schema",
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
    install._catalog_setup._ws.catalogs.get.side_effect = NotFound("test")
    install._catalog_setup._ws.schemas.get.side_effect = NotFound("schema")
    install.configure()


def test_create_catalog_no(ws, mock_installation):
    prompts = MockPrompts(
        {
            r"Select the source": "0",
            r"Do you want to Skip Validation": "yes",
            r"Enter catalog_name": "test",
            r".*Do you want to create a new one?": "yes",
            r".*": "",
        }
    )
    install = WorkspaceInstaller(prompts, mock_installation, ws)
    install._catalog_setup._ws.catalogs.get.side_effect = NotFound("test")
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
            r".*Do you want to create a new Schema?": "yes",
            r".*": "",
        }
    )
    install = WorkspaceInstaller(prompts, mock_installation, ws)
    install._catalog_setup._ws.schemas.get.side_effect = NotFound("test.schema")
    with pytest.raises(SystemExit):
        install.configure()


def test_workspace_installation(ws, mock_installation, monkeypatch):
    # Create a mock for the current method of the Installation
    mock_current = MagicMock(return_value=mock_installation)

    # Set the return value of the current method of the Installation mock
    mock_installation.current = mock_current

    # Create a mock for the Installation
    mock_install = create_autospec(Installation)

    # Use monkeypatch to replace the Installation class with our mock in the context of this test
    monkeypatch.setattr("databricks.labs.remorph.install.Installation", mock_install)

    # Call the current function
    result = WorkspaceInstallation.current(ws)

    # Assert that the result is an instance of WorkspaceInstallation
    assert isinstance(result, WorkspaceInstallation)
