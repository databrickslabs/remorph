from unittest.mock import create_autospec, patch

import pytest
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import iam

from databricks.labs.remorph import uninstall
from databricks.labs.remorph.contexts.application import CliContext
from databricks.labs.remorph.deployment.installation import WorkspaceInstallation


@pytest.fixture
def ws():
    w = create_autospec(WorkspaceClient)
    w.current_user.me.side_effect = lambda: iam.User(
        user_name="me@example.com", groups=[iam.ComplexValue(display="admins")]
    )
    return w


def test_uninstaller_run(ws):
    ctx = CliContext(ws)
    installation = create_autospec(WorkspaceInstallation)
    with patch("databricks.labs.remorph.uninstall.WorkspaceInstallation", return_value=installation):
        uninstall.run(ctx)
        installation.uninstall.assert_called_once()
