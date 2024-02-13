from datetime import timedelta
from unittest.mock import create_autospec

import pytest
from databricks.labs.blueprint.installation import Installation
from databricks.labs.blueprint.tui import MockPrompts
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import iam

from databricks.labs.remorph.config import MorphConfig
from databricks.labs.remorph.install import WorkspaceInstallation


@pytest.fixture
def ws():
    ws = create_autospec(WorkspaceClient)

    ws.current_user.me = lambda: iam.User(user_name="me@example.com", groups=[iam.ComplexValue(display="admins")])
    ws.config.host = "https://foo"

    return ws


def test_uninstall(ws):

    prompts = MockPrompts(
        {
            r"Do you want to uninstall remorph.*": "yes",
        }
    )
    installation = create_autospec(Installation)
    config = MorphConfig(source="snowflake", sdk_config=None, skip_validation=True, catalog_name="remorph_test")
    timeout = timedelta(seconds=1)

    workspace_installation = WorkspaceInstallation(config, installation, ws, prompts, timeout)

    workspace_installation.uninstall()
