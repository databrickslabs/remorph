import json
from unittest.mock import MagicMock, patch

import pytest
from pyspark.sql.session import SparkSession

from databricks.connect.session import DatabricksSession
from databricks.labs.blueprint.installation import MockInstallation
from databricks.labs.blueprint.tui import MockPrompts
from databricks.labs.remorph.config import TableRecon
from databricks.labs.remorph.helpers.reconcile_config_utils import (
    ReconcileConfigUtils,
)
from databricks.labs.remorph.reconcile.recon_config import Table
from databricks.sdk.errors.platform import ResourceDoesNotExist
from databricks.sdk.service.workspace import SecretScope

from ..reconcile.connectors.test_snowflake import mock_secret

SOURCE_DICT = {"databricks": "0", "oracle": "1", "snowflake": "2"}

SCOPE_NAME = "scope"


@pytest.fixture
def mock_installation():
    return MockInstallation(
        {
            "reconcile.yml": {
                "data_source": "snowflake",
                "config": {
                    "source_catalog": "sf_catalog",
                    "source_schema": "sf_schema",
                    "target_catalog": "db_catalog",
                    "target_schema": "db_schema",
                },
                "report_type": "schema",
                "secret_scope": SCOPE_NAME,
                "tables": {
                    "filter_type": "include",
                    "tables_list": ["orders"],
                },
                "version": 1,
            },
        }
    )


def test_configure_secrets_snowflake_overwrite(mock_workspace_client, mock_installation):
    prompts = MockPrompts(
        {
            r"Select the Data Source": SOURCE_DICT["snowflake"],
            r"Enter Secret Scope name": SCOPE_NAME,
            r"Enter Snowflake URL": "dummy",
            r"Enter Account Name": "dummy",
            r"Enter User": "dummy",
            r"Enter Password": "dummy",
            r"Enter Catalog": "dummy",
            r"Enter Schema": "dummy",
            r"Enter Snowflake Warehouse": "dummy",
            r"Enter Role": "dummy",
            r"Do you want to overwrite.*": "yes",
        }
    )
    mock_workspace_client.secrets.list_scopes.side_effect = [[SecretScope(name=SCOPE_NAME)]]
    reconcile_utils = ReconcileConfigUtils(mock_workspace_client, mock_installation, prompts=prompts)
    reconcile_utils.prompt_source()

    reconcile_utils.prompt_and_save_connection_details()
    mock_workspace_client.secrets.get_secret.assert_called()
    mock_workspace_client.secrets.put_secret.assert_called()


def test_configure_secrets_oracle_insert(mock_workspace_client, mock_installation):
    # mock prompts for Oracle
    prompts = MockPrompts(
        {
            r"Select the Data Source": SOURCE_DICT["oracle"],
            r"Enter Secret Scope name": SCOPE_NAME,
            r"Do you want to create a new one?": "yes",
            r"Enter User": "dummy",
            r"Enter Password": "dummy",
            r"Enter host": "dummy",
            r"Enter port": "dummy",
            r"Enter database/SID": "dummy",
        }
    )

    mock_workspace_client.secrets.list_scopes.side_effect = [[SecretScope(name="other_scope")]]

    with patch(
        "databricks.labs.remorph.helpers.reconcile_config_utils.ReconcileConfigUtils._secret_key_exists",
        return_value=False,
    ):
        reconcile_utils = ReconcileConfigUtils(mock_workspace_client, mock_installation, prompts=prompts)
        reconcile_utils.prompt_source()

        reconcile_utils.prompt_and_save_connection_details()
        mock_workspace_client.secrets.put_secret.assert_called()


def test_configure_secrets_invalid_source(mock_workspace_client, mock_installation):
    prompts = MockPrompts(
        {
            r"Select the Data Source": "3",
        }
    )

    reconcile_utils = ReconcileConfigUtils(mock_workspace_client, mock_installation, prompts=prompts)
    with pytest.raises(ValueError, match="cannot get answer within 10 attempt"):
        reconcile_utils.prompt_source()


def test_store_connection_secrets_exception(mock_workspace_client, mock_installation):
    prompts = MockPrompts(
        {
            r"Do you want to overwrite `source_key`?": "no",
        }
    )

    mock_workspace_client.secrets.get_secret.side_effect = ResourceDoesNotExist("Not Found")
    mock_workspace_client.secrets.put_secret.side_effect = Exception("Timed out")

    reconcile_utils = ReconcileConfigUtils(mock_workspace_client, mock_installation, prompts=prompts)

    with pytest.raises(Exception, match="Timed out"):
        reconcile_utils.store_connection_secrets("scope_name", ("source", {"key": "value"}))


def test_configure_secrets_no_scope(mock_workspace_client, mock_installation):
    prompts = MockPrompts(
        {
            r"Select the Data Source": SOURCE_DICT["snowflake"],
            r"Enter Secret Scope name": SCOPE_NAME,
            r"Do you want to create a new one?": "no",
        }
    )

    mock_workspace_client.secrets.list_scopes.side_effect = [[SecretScope(name="scope_name")]]

    reconcile_utils = ReconcileConfigUtils(mock_workspace_client, mock_installation, prompts=prompts)
    reconcile_utils.prompt_source()

    with pytest.raises(SystemExit, match="Scope is needed to store Secrets in Databricks Workspace"):
        reconcile_utils.prompt_and_save_connection_details()


def test_configure_secrets_create_scope_exception(mock_workspace_client, mock_installation):
    prompts = MockPrompts(
        {
            r"Select the Data Source": SOURCE_DICT["snowflake"],
            r"Enter Secret Scope name": SCOPE_NAME,
            r"Do you want to create a new one?": "yes",
        }
    )

    mock_workspace_client.secrets.list_scopes.side_effect = [[SecretScope(name="scope_name")]]
    mock_workspace_client.secrets.create_scope.side_effect = RuntimeError("Network Error")

    reconcile_utils = ReconcileConfigUtils(mock_workspace_client, mock_installation, prompts=prompts)
    reconcile_utils.prompt_source()

    with pytest.raises(RuntimeError, match="Network Error"):
        reconcile_utils.prompt_and_save_connection_details()


def test_store_connection_secrets_overwrite_no(mock_workspace_client, mock_installation):
    prompts = MockPrompts(
        {
            r"Do you want to overwrite `source_key`?": "no",
        }
    )

    with patch(
        "databricks.labs.remorph.helpers.reconcile_config_utils.ReconcileConfigUtils._secret_key_exists",
        return_value=True,
    ):
        reconcile_utils = ReconcileConfigUtils(mock_workspace_client, mock_installation, prompts=prompts)
        reconcile_utils.store_connection_secrets("scope_name", ("source", {"key": "value"}))
        mock_workspace_client.secrets.put_secret.assert_not_called()


def test_generate_recon_config_no_secrets_configured(mock_workspace_client, mock_installation):
    prompts = MockPrompts(
        {
            r"Would you like to overwrite workspace.*": "no",
            r"Did you setup the secrets for the.*": "no",
        }
    )

    reconcile_utils = ReconcileConfigUtils(mock_workspace_client, mock_installation, prompts=prompts)

    error_msg = (
        "Error: Secrets are needed for `Snowflake` reconciliation.\n"
        "Use `remorph configure-secrets` to setup Scope and Secrets."
    )

    mock_workspace_client.secrets.list_scopes.side_effect = [[SecretScope(name=SCOPE_NAME)]]
    with pytest.raises(ValueError, match=error_msg):
        reconcile_utils.generate_recon_config()


def test_generate_recon_config_create_scope_no(mock_workspace_client, mock_installation):
    prompts = MockPrompts(
        {
            r"Would you like to overwrite workspace.*": "no",
            r"Do you want to create a new one?": "no",
        }
    )

    reconcile_utils = ReconcileConfigUtils(mock_workspace_client, mock_installation, prompts=prompts)
    error_msg = "Scope is needed to store Secrets in Databricks Workspace"

    with pytest.raises(SystemExit, match=error_msg):
        reconcile_utils.generate_recon_config()


def test_recon_config_prompt_and_save_config_details(mock_workspace_client, mock_installation):
    prompts = MockPrompts(
        {
            r"Would you like to overwrite workspace.*": "no",
            r".*Did you setup the secrets for the": "yes",
            r"Would you like to run reconciliation.*": "yes",
            r"Open.* config file in the browser?": "no",
            r"Open `README_RECON_CONFIG` setup instructions in your browser?": "no",
        }
    )

    filename = "recon_conf_snowflake.json"
    mock_workspace_client.secrets.get_secret.side_effect = mock_secret
    recon_confing = TableRecon(
        source_schema="src_schema",
        source_catalog="src_catalog",
        target_catalog="tgt_catalog",
        target_schema="tgt_schema",
        tables=[Table(source_name="table1", target_name="table1"), Table(source_name="table2", target_name="table2")],
    )

    # Patch the scope_exists method to return True
    mock_workspace_client.secrets.list_scopes.side_effect = [[SecretScope(name=SCOPE_NAME)]]
    # Patch the builder method to return a SparkSession
    with patch.object(DatabricksSession, "builder", MagicMock(return_value=SparkSession.builder)):
        reconcile_utils = ReconcileConfigUtils(mock_workspace_client, installation=mock_installation, prompts=prompts)

        reconcile_utils.generate_recon_config()

    raw = json.dumps(recon_confing, default=vars, indent=2, sort_keys=True).encode("utf-8")

    target = mock_installation.upload(filename, raw)

    assert target == f"~/mock/{filename}"

    mock_installation.assert_file_uploaded(filename)


def test_generate_recon_config_no_reconcile(mock_workspace_client):
    corrupted_reconcile_config = MockInstallation(
        {
            "reconcile.yml": {
                "config": {
                    "source_catalog": "sf_catalog",
                    "source_schema": "sf_schema",
                    "target_catalog": "db_catalog",
                    "target_schema": "db_schema",
                },
                "report_type": "schema",
                "secret_scope": SCOPE_NAME,
                "tables": {
                    "filter_type": "include",
                    "tables_list": ["orders"],
                },
                "version": 1,
            },
        }
    )

    reconcile_utils = ReconcileConfigUtils(mock_workspace_client,
                                           installation=corrupted_reconcile_config,
                                           prompts=MockPrompts({}))

    assert reconcile_utils.generate_recon_config() is None

