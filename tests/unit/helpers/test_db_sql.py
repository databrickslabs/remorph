from unittest.mock import patch

import pytest
from databricks.sdk.errors.base import DatabricksError

from databricks.labs.remorph.helpers.db_sql import get_sql_backend


@pytest.mark.usefixtures("mock_workspace_client", "morph_config")
@patch('databricks.labs.remorph.helpers.db_sql.StatementExecutionBackend')
def test_get_sql_backend_with_warehouse_id(
    stmt_execution_backend,
    mock_workspace_client,
    morph_config,
):
    mock_workspace_client.config.warehouse_id = "test_warehouse_id"
    sql_backend = get_sql_backend(mock_workspace_client, morph_config)
    stmt_execution_backend.assert_called_once_with(
        mock_workspace_client,
        "test_warehouse_id",
        catalog=morph_config.catalog_name,
        schema=morph_config.schema_name,
    )
    assert isinstance(sql_backend, stmt_execution_backend.return_value.__class__)


@pytest.mark.usefixtures("mock_workspace_client", "morph_config")
@patch('databricks.labs.remorph.helpers.db_sql.DatabricksConnectBackend')
def test_get_sql_backend_without_warehouse_id(
    databricks_connect_backend,
    mock_workspace_client,
    morph_config,
):
    mock_dbc_backend_instance = databricks_connect_backend.return_value
    sql_backend = get_sql_backend(mock_workspace_client, morph_config)
    databricks_connect_backend.assert_called_once_with(mock_workspace_client)
    mock_dbc_backend_instance.execute.assert_any_call(f"use catalog {morph_config.catalog_name}")
    mock_dbc_backend_instance.execute.assert_any_call(f"use {morph_config.schema_name}")
    assert isinstance(sql_backend, databricks_connect_backend.return_value.__class__)


@pytest.mark.usefixtures("mock_workspace_client", "morph_config")
@patch('databricks.labs.remorph.helpers.db_sql.DatabricksConnectBackend')
def test_get_sql_backend_with_error(
    databricks_connect_backend,
    mock_workspace_client,
    morph_config,
):
    mock_dbc_backend_instance = databricks_connect_backend.return_value
    mock_dbc_backend_instance.execute.side_effect = DatabricksError("Test error")
    with pytest.raises(DatabricksError):
        get_sql_backend(mock_workspace_client, morph_config)
