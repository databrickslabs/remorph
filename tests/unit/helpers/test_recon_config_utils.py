# pylint: disable=wrong-import-order,ungrouped-imports,useless-suppression
from unittest.mock import patch

import pytest
from databricks.labs.blueprint.tui import MockPrompts

from databricks.labs.remorph.helpers.recon_config_utils import ReconConfigPrompts


def test_configure_secrets_snowflake_overwrite(mock_workspace_client):
    source_dict = {"databricks": "0", "netezza": "1", "oracle": "2", "snowflake": "3"}
    scope_name = "dummy_scope"
    prompts = MockPrompts(
        {
            r"Select the source": source_dict["snowflake"],
            r"Enter Secret Scope name": scope_name,
            r"Enter Snowflake URL": "dummy",
            r"Enter Account Name": "dummy",
            r"Enter User": "dummy",
            r"Enter Password": "dummy",
            r"Enter Database": "dummy",
            r"Enter Schema": "dummy",
            r"Enter Snowflake Warehouse": "dummy",
            r"Enter Role": "dummy",
            r"Do you want to overwrite.*": "yes",
        }
    )

    with patch(
        "databricks.labs.remorph.helpers.db_workspace_utils.DatabricksSecretsClient._scope_exists",
        return_value=True,
    ):
        recon_conf = ReconConfigPrompts(mock_workspace_client, prompts)
        recon_conf.prompt_source()

        recon_conf.prompt_and_save_connection_details()


def test_configure_secrets_oracle_insert(mock_workspace_client):
    source_dict = {"databricks": "0", "netezza": "1", "oracle": "2", "snowflake": "3"}
    scope_name = "dummy_scope"
    # mock prompts for Oracle
    prompts = MockPrompts(
        {
            r"Select the source": source_dict["oracle"],
            r"Enter Secret Scope name": scope_name,
            r"Enter User": "dummy",
            r"Enter Password": "dummy",
            r"Enter host": "dummy",
            r"Enter port": "dummy",
            r"Enter database/SID": "dummy",
        }
    )

    with patch(
        "databricks.labs.remorph.helpers.db_workspace_utils.DatabricksSecretsClient._scope_exists",
        return_value=True,
    ):
        # mock secret_key_exists to return True
        with patch(
            "databricks.labs.remorph.helpers.db_workspace_utils.DatabricksSecretsClient.secret_key_exists",
            return_value=False,
        ):
            recon_conf = ReconConfigPrompts(mock_workspace_client, prompts)
            recon_conf.prompt_source()

            recon_conf.prompt_and_save_connection_details()


def test_configure_secrets_invalid_source(mock_workspace_client):
    source_dict = {"databricks": "0", "netezza": "1", "oracle": "2", "snowflake": "3"}
    scope_name = "dummy_scope"
    # mock prompts for Oracle
    prompts = MockPrompts(
        {
            r"Select the source": source_dict["netezza"],
            r"Enter Secret Scope name": scope_name,
        }
    )

    with patch(
        "databricks.labs.remorph.helpers.db_workspace_utils.DatabricksSecretsClient._scope_exists",
        return_value=True,
    ):
        recon_conf = ReconConfigPrompts(mock_workspace_client, prompts)
        recon_conf.prompt_source()

        with pytest.raises(ValueError, match="Source netezza is not yet configured..."):
            recon_conf.prompt_and_save_connection_details()
