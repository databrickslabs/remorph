from datetime import timedelta
from unittest.mock import create_autospec, patch

import pytest

from databricks.labs.blueprint.installation import Installation, MockInstallation
from databricks.labs.blueprint.tui import MockPrompts
from databricks.labs.remorph.config import (
    MorphConfig,
    RemorphConfigs,
    ReconcileConfig,
    DatabaseConfig,
    ReconcileMetadataConfig,
)
from databricks.labs.remorph.uninstall import WorkspaceUnInstallation, WorkspaceUnInstaller
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import NotFound
from databricks.sdk.errors.platform import PermissionDenied


@pytest.fixture
def ws():
    return create_autospec(WorkspaceClient)


@pytest.fixture
def mock_installation():
    return MockInstallation(
        {
            "config.yml": {
                "source": "oracle",
                "version": 1,
            },
            "reconcile.yml": {
                "data_source": "oracle",
                "database_config": {
                    "source_schema": "tpch",
                    "target_catalog": "test",
                    "target_schema": "uninstall",
                },
                "report_type": "row",
                "secret_scope": "rmp_oracle",
                "tables": {
                    "filter_type": "exclude",
                    "tables_list": ["SUPPLIER", "FRIENDS", "ORDERS", "PART"],
                },
                "metadata_config": {
                    "catalog": "rmp",
                    "schema": "rcn",
                    "volume": "test_volume",
                },
                "version": 1,
            },
        }
    )


def test_ws_uninstall(ws):
    prompts = MockPrompts(
        {
            r"Do you want to uninstall .*": "yes",
        }
    )
    ws.jobs.delete.return_value = None
    installation = create_autospec(Installation)

    morph = MorphConfig(source="snowflake")
    db_config = DatabaseConfig(
        source_schema="source_schema",
        target_catalog="target_catalog",
        target_schema="target_schema",
        source_catalog=None,
    )

    reconcile = ReconcileConfig(
        data_source="snowflake",
        report_type="reconcile",
        secret_scope="remorph_test",
        database_config=db_config,
        metadata_config=ReconcileMetadataConfig(),
        job_id="123",
        tables=None,
    )

    configs = RemorphConfigs(morph, reconcile)

    uninstaller = WorkspaceUnInstallation(configs, installation, ws, prompts, timedelta(seconds=1))
    assert uninstaller.uninstall()

    # Assert that the `uninstaller` is an instance of WorkspaceUnInstallation
    assert isinstance(uninstaller, WorkspaceUnInstallation)


def test_uninstall_no_remorph_dir(ws):
    prompts = MockPrompts(
        {
            r"Do you want to uninstall .*": "yes",
        }
    )
    mock_installation_reconcile = MockInstallation(
        {
            "reconcile.yml": {
                "data_source": "oracle",
                "database_config": {
                    "source_schema": "tpch",
                    "target_catalog": "test",
                    "target_schema": "uninstall",
                },
                "report_type": "row",
                "secret_scope": "rmp_oracle",
                "tables": {
                    "filter_type": "exclude",
                    "tables_list": ["SUPPLIER", "FRIENDS", "ORDERS", "PART"],
                },
                "metadata_config": {
                    "catalog": "rmp",
                    "schema": "rcn",
                    "volume": "test_volume",
                },
                "version": 1,
            },
        }
    )
    with patch.object(mock_installation_reconcile, "files", side_effect=NotFound):
        uninstaller = WorkspaceUnInstaller(mock_installation_reconcile, ws, prompts, timedelta(seconds=1))

        assert uninstaller.uninstall() is False

        # Assert that the `uninstaller` is an instance of WorkspaceUnInstaller
        assert isinstance(uninstaller, WorkspaceUnInstaller)


def test_uninstall_no(ws):
    prompts = MockPrompts(
        {
            r"Do you want to uninstall .*": "no",
        }
    )
    mock_installation_morph = MockInstallation(
        {
            "config.yml": {
                "source": "oracle",
                "version": 1,
            },
        }
    )
    uninstaller = WorkspaceUnInstaller(mock_installation_morph, ws, prompts, timedelta(seconds=1))

    assert uninstaller.uninstall() is False


def test_uninstall_no_permissions(ws):
    prompts = MockPrompts(
        {
            r"Do you want to uninstall .*": "no",
        }
    )
    empty_installation = MockInstallation({})
    with patch.object(empty_installation, "load", side_effect=PermissionDenied):
        uninstaller = WorkspaceUnInstaller(empty_installation, ws, prompts, timedelta(seconds=1))

        assert uninstaller.uninstall() is False


def test_uninstall(ws, mock_installation):
    prompts = MockPrompts(
        {
            r"Do you want to uninstall .*": "yes",
        }
    )

    uninstaller = WorkspaceUnInstaller(mock_installation, ws, prompts, timedelta(seconds=1))

    assert uninstaller.uninstall()

    # Assert that the `uninstaller` is an instance of WorkspaceUnInstallation
    assert isinstance(uninstaller, WorkspaceUnInstaller)
