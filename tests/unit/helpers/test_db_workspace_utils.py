# pylint: disable=protected-access
from unittest.mock import patch

import pytest
from databricks.labs.blueprint.tui import MockPrompts
from databricks.sdk.service.workspace import SecretScope

from databricks.labs.remorph.helpers.db_workspace_utils import DatabricksSecretsClient


@pytest.fixture
def db_secrets_client(mock_workspace_client):
    return DatabricksSecretsClient(
        mock_workspace_client,
        prompts=MockPrompts(
            {
                r"Do you want to create a new one?": "yes",
                r".*": "",
            }
        ),
    )


def test_scope_exists(db_secrets_client):
    with patch.object(db_secrets_client._ws.secrets, 'list_scopes', return_value=[SecretScope(name="scope_name")]):
        assert db_secrets_client._scope_exists("scope_name")


def test_get_or_create_scope(db_secrets_client):
    with patch.object(db_secrets_client._ws.secrets, 'create_scope', return_value={}):
        db_secrets_client.get_or_create_scope("scope_name")


def test_get_or_create_scope_exception(db_secrets_client):
    with patch.object(db_secrets_client._ws.secrets, 'create_scope', side_effect=Exception()):
        with pytest.raises(Exception):
            db_secrets_client.get_or_create_scope("scope_name")
