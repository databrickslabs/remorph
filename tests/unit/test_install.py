import os
from unittest.mock import create_autospec

import pytest
from databricks.labs.blueprint.installation import MockInstallation
from databricks.labs.blueprint.tui import MockPrompts
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import NotFound

from databricks.labs.remorph.__about__ import __version__
from databricks.labs.remorph.install import WorkspaceInstaller


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
            r"Do you want to Skip Validation": "1",
            r"Enter catalog_name": "remorph_test",
            r"Enter schema_name": "remorph_schema",
            r".*": "",
        }
    )
    install = WorkspaceInstaller(prompts, mock_installation, ws)
    install.run()


def test_install_dbr(ws, mock_installation):
    os.environ["DATABRICKS_RUNTIME_VERSION"] = "14.1"
    prompts = MockPrompts(
        {
            r"Select the source": "0",
            r"Do you want to Skip Validation": "1",
            r".*": "",
        }
    )
    with pytest.raises(SystemExit):
        install = WorkspaceInstaller(prompts, mock_installation, ws)
        install.run()
    del os.environ["DATABRICKS_RUNTIME_VERSION"]


def test_save_config(ws, mock_installation):
    prompts = MockPrompts(
        {
            r"Select the source": "0",
            r"Do you want to Skip Validation": "1",
            r"Enter catalog_name": "remorph_catalog",
            r"Enter schema_name": "remorph_schema",
            r".*": "",
        }
    )
    install = WorkspaceInstaller(prompts, mock_installation, ws)
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
            r"Do you want to Skip Validation": "1",
            r"Enter catalog_name": "test",
            r".*Do you want to create a new one?": True,
            r"Enter schema_name": "schema",
            r".*Do you want to create a new Schema?": True,
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
            r"Do you want to Skip Validation": "1",
            r"Enter catalog_name": "test",
            r".*Do you want to create a new one?": False,
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
            r"Do you want to Skip Validation": "1",
            r"Enter catalog_name": "test",
            r".*Do you want to create a new one?": True,
            r"Enter schema_name": "schema",
            r".*Do you want to create a new Schema?": False,
            r".*": "",
        }
    )
    install = WorkspaceInstaller(prompts, mock_installation, ws)
    install._catalog_setup._ws.schemas.get.side_effect = NotFound("test.schema")
    with pytest.raises(SystemExit):
        install.configure()
