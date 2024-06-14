from unittest.mock import patch

import pytest
from databricks.labs.remorph.helpers.db_sql import get_sql_backend


@pytest.fixture()
def morph_config_sql_backend(morph_config):
    return morph_config


@patch('databricks.labs.remorph.helpers.db_sql.StatementExecutionBackend')
def test_get_sql_backend_with_warehouse_id(
    stmt_execution_backend,
    mock_workspace_client,
    morph_config_sql_backend,
):
    morph_config_sql_backend.sdk_config = {"warehouse_id": "test_warehouse_id"}
    sql_backend = get_sql_backend(mock_workspace_client, morph_config_sql_backend)
    stmt_execution_backend.assert_called_once_with(
        mock_workspace_client,
        "test_warehouse_id",
        catalog=morph_config_sql_backend.catalog_name,
        schema=morph_config_sql_backend.schema_name,
    )
    assert isinstance(sql_backend, stmt_execution_backend.return_value.__class__)


@patch('databricks.labs.remorph.helpers.db_sql.DatabricksConnectBackend')
def test_get_sql_backend_without_warehouse_id(
    databricks_connect_backend,
    mock_workspace_client,
    morph_config_sql_backend,
):
    # morph config mock object has cluster id
    sql_backend = get_sql_backend(mock_workspace_client, morph_config_sql_backend)
    databricks_connect_backend.assert_called_once_with(mock_workspace_client)
    assert isinstance(sql_backend, databricks_connect_backend.return_value.__class__)


@pytest.mark.usefixtures("monkeypatch")
@patch('databricks.labs.remorph.helpers.db_sql.RuntimeBackend')
def test_get_sql_backend_without_warehouse_id_in_notebook(
    runtime_backend,
    mock_workspace_client,
    morph_config_sql_backend,
    monkeypatch,
):
    monkeypatch.setenv("DATABRICKS_RUNTIME_VERSION", "14.3")
    morph_config_sql_backend.sdk_config = None
    sql_backend = get_sql_backend(mock_workspace_client, morph_config_sql_backend)
    runtime_backend.assert_called_once()
    assert isinstance(sql_backend, runtime_backend.return_value.__class__)
