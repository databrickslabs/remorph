# pylint: disable=wrong-import-order,ungrouped-imports,useless-suppression
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from databricks.connect.session import DatabricksSession
from databricks.labs.blueprint.tui import MockPrompts
from pyspark.sql.session import SparkSession

from databricks.labs.remorph.helpers.recon_config_utils import ReconConfigPrompts


def test_generate_recon_config_no_secrets_configured(mock_workspace_client):
    source_dict = {"databricks": "0", "netezza": "1", "oracle": "2", "snowflake": "3"}

    prompts = MockPrompts(
        {
            r"Select the source": source_dict["snowflake"],
            r".*Did you setup the secrets for the": "no",
        }
    )

    recon_conf = ReconConfigPrompts(mock_workspace_client, prompts)
    recon_conf.prompt_source()

    error_msg = (
        "Error: Secrets are needed for `snowflake` reconciliation.\n"
        "Use `remorph configure-secrets` to setup Scope and Secrets."
    )

    with pytest.raises(ValueError, match=error_msg):
        recon_conf.prompt_and_save_config_details()


def test_generate_recon_config_create_scope_no(mock_workspace_client):
    source_dict = {"databricks": "0", "netezza": "1", "oracle": "2", "snowflake": "3"}

    prompts = MockPrompts(
        {
            r"Select the source": source_dict["snowflake"],
            r".*Did you setup the secrets for the": "yes",
            r"Enter Secret Scope name": "dummy",
            r"Do you want to create a new one?": "no",
        }
    )

    recon_conf = ReconConfigPrompts(mock_workspace_client, prompts)
    recon_conf.prompt_source()

    error_msg = "Scope is needed to store Secrets in Databricks Workspace"

    with pytest.raises(SystemExit, match=error_msg):
        recon_conf.prompt_and_save_config_details()


def test_recon_config_prompt_and_save_config_details(mock_workspace_client):
    source_dict = {"databricks": "0", "netezza": "1", "oracle": "2", "snowflake": "3"}
    filter_dict = {"exclude": "0", "include": "1"}

    prompts = MockPrompts(
        {
            r"Select the source": source_dict["snowflake"],
            r".*Did you setup the secrets for the": "yes",
            r"Enter Secret Scope name": "dummy",
            r"Enter `snowflake` catalog_name": "sf_catalog",
            r"Enter `snowflake` database_name": "sf_schema",
            r"Enter target catalog_name": "tgt_catalog",
            r"Enter target schema_name": "tgt_schema",
            r"Do you want to include/exclude a set of tables?": "yes",
            r"Select the filter type": filter_dict["include"],
            r"Enter the tables(separated by comma) to `include`": "table1, table2",
            r".*": "",
        }
    )

    # Patch the scope_exists method to return True
    with patch(
        "databricks.labs.remorph.helpers.db_workspace_utils.DatabricksSecretsClient._scope_exists",
        return_value=True,
    ):
        # Patch the builder method to return a SparkSession
        with patch.object(DatabricksSession, "builder", MagicMock(return_value=SparkSession.builder)):
            recon_conf = ReconConfigPrompts(mock_workspace_client, prompts)
            recon_conf.prompt_source()

            recon_conf.prompt_and_save_config_details()

            # Check that the config file is created
            assert Path("./recon_conf_snowflake.json").exists()

            # Check the contents of the config file
            with open(Path("./recon_conf_snowflake.json"), "r", encoding="utf-8") as file:
                content = file.read().strip()
                reconf_config = json.loads(content)
                assert reconf_config["source_catalog"] == "sf_catalog", "Source catalog name is incorrect"
                assert reconf_config["source_schema"] == "sf_schema", "Source schema name is incorrect"
                assert reconf_config["target_catalog"] == "tgt_catalog", "Target catalog name is incorrect"
                assert reconf_config["target_schema"] == "tgt_schema", "Target schema name is incorrect"

            Path("./recon_conf_snowflake.json").unlink()


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
