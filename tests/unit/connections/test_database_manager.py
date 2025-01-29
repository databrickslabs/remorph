import pytest
from unittest.mock import MagicMock, patch
from databricks.labs.remorph.connections.database_manager import DatabaseManager

sample_config = {
    'user': 'test_user',
    'password': 'test_pass',
    'server': 'test_server',
    'database': 'test_db',
    'driver': 'ODBC Driver 17 for SQL Server',
}


def test_create_connector_unsupported_db_type():
    with pytest.raises(ValueError, match="Unsupported database type: unsupported_db"):
        DatabaseManager("unsupported_db", sample_config)


# Test case for MSSQLConnector
@patch('databricks.labs.remorph.connections.database_manager.MSSQLConnector')
def test_mssql_connector(mock_mssql_connector):
    mock_connector_instance = MagicMock()
    mock_mssql_connector.return_value = mock_connector_instance

    db_manager = DatabaseManager("mssql", sample_config)

    assert db_manager.connector == mock_connector_instance
    mock_mssql_connector.assert_called_once_with(sample_config)


@patch('databricks.labs.remorph.connections.database_manager.MSSQLConnector')
def test_execute_query(mock_mssql_connector):
    mock_connector_instance = MagicMock()
    mock_mssql_connector.return_value = mock_connector_instance

    db_manager = DatabaseManager("mssql", sample_config)

    query = "SELECT * FROM users"
    mock_result = MagicMock()
    mock_connector_instance.execute_query.return_value = mock_result

    result = db_manager.execute_query(query)

    assert result == mock_result
    mock_connector_instance.execute_query.assert_called_once_with(query)


def test_execute_query_without_connection():
    db_manager = DatabaseManager("mssql", sample_config)

    # Simulating that the engine is not connected
    db_manager.connector.engine = None

    with pytest.raises(ConnectionError, match="Not connected to the database."):
        db_manager.execute_query("SELECT * FROM users")
