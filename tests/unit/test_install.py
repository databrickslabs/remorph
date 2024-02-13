from unittest.mock import create_autospec

import pytest
from databricks.labs.blueprint.installation import MockInstallation
from databricks.labs.blueprint.tui import MockPrompts
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import iam

from databricks.labs.remorph.install import WorkspaceInstaller


@pytest.fixture
def ws():
    ws = create_autospec(WorkspaceClient)

    ws.current_user.me = lambda: iam.User(user_name="me@example.com", groups=[iam.ComplexValue(display="admins")])
    ws.config.host = "https://foo"

    return ws


@pytest.fixture
def mock_installation():
    return MockInstallation(
        {"state.json": {"version": 1, "source": "snowflake", "skip_validation": True, "catalog_name": "remorph_test"}}
    )


def test_save_config(ws, mock_installation):

    prompts = MockPrompts(
        {
            r"Select the source": "0",
            r"Do you want to Skip Validation": "1",
            r".*": "",
        }
    )
    install = WorkspaceInstaller(prompts, mock_installation, ws)
    install.configure()

    mock_installation.assert_file_written(
        "config.yml",
        {"version": 1, "source": "snowflake", "skip_validation": True},
    )
