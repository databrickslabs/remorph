import json
from unittest.mock import MagicMock, patch

import pytest
from pyspark.sql.session import SparkSession

from databricks.connect.session import DatabricksSession
from databricks.labs.blueprint.installation import MockInstallation
from databricks.labs.blueprint.tui import MockPrompts
from databricks.labs.remorph.config import TableRecon
from databricks.labs.remorph.helpers.recon_config_utils import (
    ReconConfigPrompts,
    get_data_source,
)
from databricks.labs.remorph.reconcile.constants import SourceType
from databricks.labs.remorph.reconcile.recon_config import Table
from databricks.sdk.errors.platform import ResourceDoesNotExist
from databricks.sdk.service.workspace import SecretScope

SOURCE_DICT = {"databricks": "0", "oracle": "1", "snowflake": "2"}
SCOPE_NAME = "dummy_scope"


def test_configure_secrets_snowflake_overwrite(mock_workspace_client):
    prompts = MockPrompts(
        {
            r"Select the source": SOURCE_DICT["snowflake"],
            r"Enter Secret Scope name": SCOPE_NAME,
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
    mock_workspace_client.secrets.list_scopes.side_effect = [[SecretScope(name=SCOPE_NAME)]]
    recon_conf = ReconConfigPrompts(mock_workspace_client, prompts=prompts)
    recon_conf.prompt_source()

    recon_conf.prompt_and_save_connection_details()


def test_configure_secrets_oracle_insert(mock_workspace_client):
    # mock prompts for Oracle
    prompts = MockPrompts(
        {
            r"Select the source": SOURCE_DICT["oracle"],
            r"Enter Secret Scope name": SCOPE_NAME,
            r"Do you want to create a new one?": "yes",
            r"Enter User": "dummy",
            r"Enter Password": "dummy",
            r"Enter host": "dummy",
            r"Enter port": "dummy",
            r"Enter database/SID": "dummy",
        }
    )

    mock_workspace_client.secrets.list_scopes.side_effect = [[SecretScope(name="scope_name")]]

    with patch(
            "databricks.labs.remorph.helpers.recon_config_utils.ReconConfigPrompts._secret_key_exists",
            return_value=False,
    ):
        recon_conf = ReconConfigPrompts(mock_workspace_client, prompts=prompts)
        recon_conf.prompt_source()

        recon_conf.prompt_and_save_connection_details()


def test_configure_secrets_invalid_source(mock_workspace_client):
    prompts = MockPrompts(
        {
            r"Select the source": "3",
            r"Enter Secret Scope name": SCOPE_NAME,
        }
    )

    with patch(
            "databricks.labs.remorph.helpers.recon_config_utils.ReconConfigPrompts._scope_exists",
            return_value=True,
    ):
        recon_conf = ReconConfigPrompts(mock_workspace_client, prompts=prompts)
        with pytest.raises(ValueError, match="cannot get answer within 10 attempt"):
            recon_conf.prompt_source()


def test_store_connection_secrets_exception(mock_workspace_client):
    prompts = MockPrompts(
        {
            r"Do you want to overwrite `source_key`?": "no",
        }
    )

    mock_workspace_client.secrets.get_secret.side_effect = ResourceDoesNotExist("Not Found")
    mock_workspace_client.secrets.put_secret.side_effect = Exception("Timed out")

    recon_conf = ReconConfigPrompts(mock_workspace_client, prompts=prompts)

    with pytest.raises(Exception, match="Timed out"):
        recon_conf.store_connection_secrets("scope_name", ("source", {"key": "value"}))


def test_configure_secrets_no_scope(mock_workspace_client):
    prompts = MockPrompts(
        {
            r"Select the source": SOURCE_DICT["snowflake"],
            r"Enter Secret Scope name": SCOPE_NAME,
            r"Do you want to create a new one?": "no",
        }
    )

    mock_workspace_client.secrets.list_scopes.side_effect = [[SecretScope(name="scope_name")]]

    recon_conf = ReconConfigPrompts(mock_workspace_client, prompts=prompts)
    recon_conf.prompt_source()

    with pytest.raises(SystemExit, match="Scope is needed to store Secrets in Databricks Workspace"):
        recon_conf.prompt_and_save_connection_details()


def test_configure_secrets_create_scope_exception(mock_workspace_client):
    prompts = MockPrompts(
        {
            r"Select the source": SOURCE_DICT["snowflake"],
            r"Enter Secret Scope name": SCOPE_NAME,
            r"Do you want to create a new one?": "yes",
        }
    )

    mock_workspace_client.secrets.list_scopes.side_effect = [[SecretScope(name="scope_name")]]
    mock_workspace_client.secrets.create_scope.side_effect = Exception("Network Error")

    recon_conf = ReconConfigPrompts(mock_workspace_client, prompts=prompts)
    recon_conf.prompt_source()

    with pytest.raises(Exception, match="Network Error"):
        recon_conf.prompt_and_save_connection_details()


def test_store_connection_secrets_overwrite(mock_workspace_client):
    prompts = MockPrompts(
        {
            r"Do you want to overwrite `source_key`?": "no",
        }
    )

    with patch(
            "databricks.labs.remorph.helpers.recon_config_utils.ReconConfigPrompts._secret_key_exists",
            return_value=True
    ):
        recon_conf = ReconConfigPrompts(mock_workspace_client, prompts=prompts)
        recon_conf.store_connection_secrets("scope_name", ("source", {"key": "value"}))


def test_generate_recon_config_no_secrets_configured(mock_workspace_client):
    prompts = MockPrompts(
        {
            r"Select the source": SOURCE_DICT["snowflake"],
            r".*Did you setup the secrets for the": "no",
        }
    )

    recon_conf = ReconConfigPrompts(mock_workspace_client, prompts=prompts)
    recon_conf.prompt_source()

    error_msg = (
        "Error: Secrets are needed for `snowflake` reconciliation.\n"
        "Use `remorph configure-secrets` to setup Scope and Secrets."
    )

    with pytest.raises(ValueError, match=error_msg):
        recon_conf.prompt_and_save_config_details()


def test_generate_recon_config_create_scope_no(mock_workspace_client):
    prompts = MockPrompts(
        {
            r"Select the source": SOURCE_DICT["snowflake"],
            r".*Did you setup the secrets for the": "yes",
            r"Enter Secret Scope name": "dummy",
            r"Do you want to create a new one?": "no",
        }
    )

    recon_conf = ReconConfigPrompts(mock_workspace_client, prompts=prompts)
    recon_conf.prompt_source()

    error_msg = "Scope is needed to store Secrets in Databricks Workspace"

    with pytest.raises(SystemExit, match=error_msg):
        recon_conf.prompt_and_save_config_details()


def test_recon_config_prompt_and_save_config_details(mock_workspace_client):
    filter_dict = {"exclude": "0", "include": "1"}

    prompts = MockPrompts(
        {
            r"Select the source": SOURCE_DICT["snowflake"],
            r".*Did you setup the secrets for the": "yes",
            r"Enter Secret Scope name": "dummy",
            r"Enter `snowflake` catalog_name": "sf_catalog",
            r"Enter `snowflake` database_name": "sf_schema",
            r"Enter target catalog_name": "tgt_catalog",
            r"Enter target schema_name": "tgt_schema",
            r"Do you want to include/exclude a set of tables?": "yes",
            r"Select the filter type": filter_dict["include"],
            r"Enter the tables.*": "table1, table2",
            r"Open.* config file in the browser?": "yes",
        }
    )

    filename = "recon_conf_snowflake.json"
    recon_confing = TableRecon(
        source_schema="src_schema",
        source_catalog="src_catalog",
        target_catalog="tgt_catalog",
        target_schema="tgt_schema",
        tables=[Table(source_name="table1", target_name="table1"), Table(source_name="table2", target_name="table2")],
    )

    installation = MockInstallation()

    # Patch the scope_exists method to return True
    mock_workspace_client.secrets.list_scopes.side_effect = [[SecretScope(name="dummy")]]
    # Patch the builder method to return a SparkSession
    with patch.object(DatabricksSession, "builder", MagicMock(return_value=SparkSession.builder)):
        # mock WorkspaceClient and Installation in _save_config_details
        with patch("databricks.labs.remorph.helpers.recon_config_utils.WorkspaceClient", mock_workspace_client):
            with patch("databricks.labs.remorph.helpers.recon_config_utils.Installation", MagicMock()):
                recon_conf = ReconConfigPrompts(mock_workspace_client, installation=installation,
                                                prompts=prompts)
                recon_conf.prompt_source()

                recon_conf.prompt_and_save_config_details()

    raw = json.dumps(recon_confing, default=vars, indent=2, sort_keys=True).encode("utf-8")

    target = installation.upload(filename, raw)

    assert target == f"~/mock/{filename}"

    installation.assert_file_uploaded(filename)


def test_get_data_source(mock_workspace_client):
    pyspark_sql_session = MagicMock()
    spark = pyspark_sql_session.SparkSession.builder.getOrCreate()

    with pytest.raises(ValueError, match="Unsupported engine: teradata"):
        get_data_source("teradata", spark, mock_workspace_client, "dummy_scope")

    snowflake_datasource = get_data_source(SourceType.SNOWFLAKE.value, spark, mock_workspace_client, "dummy_scope")

    oracle_datasource = get_data_source(SourceType.ORACLE.value, spark, mock_workspace_client, "dummy_scope")

    databricks_datasource = get_data_source(SourceType.DATABRICKS.value, spark, mock_workspace_client, "dummy_scope")

    assert snowflake_datasource and type(snowflake_datasource).__name__ == "SnowflakeDataSource"

    assert oracle_datasource and type(oracle_datasource).__name__ == "OracleDataSource"

    assert databricks_datasource and type(databricks_datasource).__name__ == "DatabricksDataSource"
