from unittest.mock import create_autospec

import pytest
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import iam

from databricks.labs.remorph import uninstall
from databricks.labs.remorph.config import RemorphConfigs
from databricks.labs.remorph.contexts.application import ApplicationContext
from databricks.labs.remorph.deployment.installation import WorkspaceInstallation


@pytest.fixture
def ws():
    w = create_autospec(WorkspaceClient)
    w.current_user.me.side_effect = lambda: iam.User(
        user_name="me@example.com", groups=[iam.ComplexValue(display="admins")]
    )
    return w


def test_uninstaller_run(ws):
    ws_installation = create_autospec(WorkspaceInstallation)
    ctx = ApplicationContext(ws)
    ctx.replace(
        workspace_installation=ws_installation,
        remorph_config=RemorphConfigs(),
    )
    uninstall.run(ctx)
    ws_installation.uninstall.assert_called_once()
