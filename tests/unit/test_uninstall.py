from datetime import timedelta
from unittest.mock import create_autospec

import pytest

from databricks.labs.blueprint.installation import Installation
from databricks.labs.blueprint.tui import MockPrompts
from databricks.labs.remorph.config import MorphConfig
from databricks.labs.remorph.uninstall import WorkspaceUnInstallation
from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import NotFound


@pytest.fixture
def ws():
    w = create_autospec(WorkspaceClient)  # pylint: disable=mock-no-usage
    return w


def test_uninstall(ws):
    prompts = MockPrompts(
        {
            r"Do you want to uninstall remorph.*": "yes",
        }
    )
    installation = create_autospec(Installation)  # pylint: disable=mock-no-usage
    config = MorphConfig(source="snowflake", sdk_config=None, skip_validation=True, catalog_name="remorph_test")
    timeout = timedelta(seconds=1)

    uninstaller = WorkspaceUnInstallation(config, installation, ws, prompts, timeout)
    uninstaller.uninstall()

    # Assert that the `uninstaller` is an instance of WorkspaceUnInstallation
    assert isinstance(uninstaller, WorkspaceUnInstallation)


def test_uninstall_no_remorph_dir(ws):
    prompts = MockPrompts(
        {
            r"Do you want to uninstall remorph.*": "yes",
        }
    )
    installation = create_autospec(Installation)
    installation.files.side_effect = NotFound()

    config = MorphConfig(source="snowflake", sdk_config=None, skip_validation=True, catalog_name="remorph_test")
    timeout = timedelta(seconds=1)

    uninstaller = WorkspaceUnInstallation(config, installation, ws, prompts, timeout)

    uninstaller.uninstall()

    # Assert that the `uninstaller` is an instance of WorkspaceUnInstallation
    assert isinstance(uninstaller, WorkspaceUnInstallation)


def test_uninstall_no(ws):
    prompts = MockPrompts(
        {
            r"Do you want to uninstall remorph.*": "no",
        }
    )
    installation = create_autospec(Installation)  # pylint: disable=mock-no-usage
    config = MorphConfig(source="snowflake", sdk_config=None, skip_validation=True, catalog_name="remorph_test")
    timeout = timedelta(seconds=1)

    uninstaller = WorkspaceUnInstallation(config, installation, ws, prompts, timeout)

    uninstaller.uninstall()

    # Assert that the `uninstaller` is an instance of WorkspaceUnInstallation
    assert isinstance(uninstaller, WorkspaceUnInstallation)
