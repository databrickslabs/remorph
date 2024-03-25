from unittest.mock import patch

import pytest
from databricks.labs.lsql.backends import MockBackend
from databricks.labs.lsql.core import Row
from databricks.sdk.errors.base import DatabricksError

from databricks.labs.remorph.helpers.validation import Validator, get_sql_backend


def test_valid_query():
    query = "SELECT * FROM a_table"
    sql_backend = MockBackend(
        rows={
            "EXPLAIN SELECT": [Row(plan="== Physical Plan ==")],
        }
    )
    validator = Validator(sql_backend)
    result, exception = validator.query(sql_backend, query)
    assert result is True
    assert exception is None


def test_query_with_syntax_error():
    query = "SELECT * a_table"
    sql_backend = MockBackend(
        fails_on_first={
            f"EXPLAIN {query}": "[PARSE_SYNTAX_ERROR] Syntax error at",
        }
    )
    validator = Validator(sql_backend)
    result, exception = validator.query(sql_backend, query)
    assert result is False
    assert "Syntax error" in exception


def test_query_with_analysis_error():
    error_types = [
        ("[TABLE_OR_VIEW_NOT_FOUND]", True),
        ("[TABLE_OR_VIEW_ALREADY_EXISTS]", True),
        ("[UNRESOLVED_ROUTINE]", False),
        ("Hive support is required to CREATE Hive TABLE (AS SELECT).;", True),
        ("Some other analysis error", False),
    ]

    for err, status in error_types:
        query = "SELECT * FROM a_table"
        sql_backend = MockBackend(
            fails_on_first={
                f"EXPLAIN {query}": err,
            }
        )
        validator = Validator(sql_backend)
        result, exception = validator.query(sql_backend, query)
        assert result is status
        assert err in exception


def test_validate_format_result_with_valid_query(morph_config):
    query = "SELECT current_timestamp()"
    sql_backend = MockBackend(
        rows={
            "EXPLAIN SELECT": [Row(plan="== Physical Plan ==")],
        }
    )
    validator = Validator(sql_backend)
    result, exception = validator.validate_format_result(morph_config, query)
    assert query in result
    assert exception is None


def test_validate_format_result_with_invalid_query(morph_config):
    query = "SELECT fn() FROM tab"
    sql_backend = MockBackend(
        rows={
            "EXPLAIN SELECT": [
                Row(plan="Error occurred during query planning:"),
                Row(plan="[UNRESOLVED_ROUTINE] Cannot resolve function"),
            ],
        }
    )
    validator = Validator(sql_backend)
    result, exception = validator.validate_format_result(morph_config, query)
    assert "Exception Start" in result
    assert "[UNRESOLVED_ROUTINE]" in exception


@pytest.mark.usefixtures("mock_workspace_client", "morph_config")
@patch('databricks.labs.remorph.helpers.validation.StatementExecutionBackend')
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
@patch('databricks.labs.remorph.helpers.validation.DatabricksConnectBackend')
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
@patch('databricks.labs.remorph.helpers.validation.DatabricksConnectBackend')
def test_get_sql_backend_with_error(
    databricks_connect_backend,
    mock_workspace_client,
    morph_config,
):
    mock_dbc_backend_instance = databricks_connect_backend.return_value
    mock_dbc_backend_instance.execute.side_effect = DatabricksError("Test error")
    with pytest.raises(DatabricksError):
        get_sql_backend(mock_workspace_client, morph_config)
