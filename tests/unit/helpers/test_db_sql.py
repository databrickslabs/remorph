from unittest.mock import create_autospec

import pytest
from databricks.labs.lsql.backends import StatementExecutionBackend, DatabricksConnectBackend, RuntimeBackend

from databricks.labs.remorph.helpers.db_sql import get_sql_backend
from databricks.sdk.errors.base import DatabricksError


@pytest.fixture()
def morph_config_sqlbackend(morph_config):
    return morph_config


def test_get_sql_backend_with_warehouse_id(
    mock_workspace_client,
    morph_config_sqlbackend,
):
    stmt_execution_backend = create_autospec(StatementExecutionBackend)
    morph_config_sqlbackend.sdk_config = {"warehouse_id": "test_warehouse_id"}
    sql_backend = get_sql_backend(
        mock_workspace_client, morph_config_sqlbackend, statement_backend=stmt_execution_backend
    )
    stmt_execution_backend.assert_called_once_with(
        mock_workspace_client,
        "test_warehouse_id",
        catalog=morph_config_sqlbackend.catalog_name,
        schema=morph_config_sqlbackend.schema_name,
    )
    assert isinstance(sql_backend, stmt_execution_backend.return_value.__class__)


def test_get_sql_backend_without_warehouse_id(
    mock_workspace_client,
    morph_config_sqlbackend,
):
    databricks_connect_backend = create_autospec(DatabricksConnectBackend)
    mock_dbc_backend_instance = databricks_connect_backend.return_value
    # morph config mock object has cluster id
    sql_backend = get_sql_backend(
        mock_workspace_client, morph_config_sqlbackend, databricks_backend=databricks_connect_backend
    )
    databricks_connect_backend.assert_called_once_with(mock_workspace_client)
    mock_dbc_backend_instance.execute.assert_any_call(f"use catalog {morph_config_sqlbackend.catalog_name}")
    mock_dbc_backend_instance.execute.assert_any_call(f"use {morph_config_sqlbackend.schema_name}")
    assert isinstance(sql_backend, databricks_connect_backend.return_value.__class__)


@pytest.mark.usefixtures("monkeypatch")
def test_get_sql_backend_without_warehouse_id_in_notebook(
    mock_workspace_client,
    morph_config_sqlbackend,
    monkeypatch,
):
    runtime_backend = create_autospec(RuntimeBackend)
    monkeypatch.setenv("DATABRICKS_RUNTIME_VERSION", "14.3")
    mock_runtime_backend_instance = runtime_backend.return_value
    morph_config_sqlbackend.sdk_config = None
    sql_backend = get_sql_backend(mock_workspace_client, morph_config_sqlbackend, runtime_backend=runtime_backend)
    runtime_backend.assert_called_once()
    mock_runtime_backend_instance.execute.assert_any_call(f"use catalog {morph_config_sqlbackend.catalog_name}")
    mock_runtime_backend_instance.execute.assert_any_call(f"use {morph_config_sqlbackend.schema_name}")
    assert isinstance(sql_backend, runtime_backend.return_value.__class__)


def test_get_sql_backend_with_error(
    mock_workspace_client,
    morph_config_sqlbackend,
):
    databricks_connect_backend = create_autospec(DatabricksConnectBackend)
    mock_dbc_backend_instance = databricks_connect_backend.return_value
    databricks_connect_backend.fetch.return_value = []
    mock_dbc_backend_instance.execute.side_effect = DatabricksError("Test error")
    with pytest.raises(DatabricksError):
        get_sql_backend(mock_workspace_client, morph_config_sqlbackend, databricks_backend=databricks_connect_backend)
