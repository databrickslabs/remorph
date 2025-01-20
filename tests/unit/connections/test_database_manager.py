import pytest
from unittest.mock import create_autospec, patch

from databricks.labs.remorph.connections.database_manager import DatabaseManager, MSSQLConnector

def test_unsupported_database_type():
    config = {'user': 'user', 'password': 'password', 'server': 'server', 'database': 'database', 'driver': 'driver'}
    with pytest.raises(ValueError, match="Unsupported database type: invalid_db"):
        DatabaseManager('invalid_db', config)

def test_mssql_connector_connection():
    config = {
        'user': 'valid_user',
        'password': 'valid_password',
        'server': 'valid_server',
        'database': 'valid_database',
        'driver': 'ODBC Driver 17 for SQL Server'
    }

    with patch('sqlalchemy.create_engine') as mock_create_engine, \
        patch.object(MSSQLConnector, '_connect', return_value=None):  # Prevent actual connection
        connector = MSSQLConnector(config)
        engine = connector._connect()

        assert engine is not None
        mock_create_engine.assert_called_once_with(
            f"mssql+pyodbc://{config['user']}:{config['password']}@{config['server']}/{config['database']}?driver={config['driver']}",
            echo=True,
            connect_args=None
        )

def test_execute_successful_query():
    config = {
        'user': 'valid_user',
        'password': 'valid_password',
        'server': 'valid_server',
        'database': 'valid_database',
        'driver': 'ODBC Driver 17 for SQL Server'
    }

    with patch('sqlalchemy.create_engine'), \
         patch('sqlalchemy.orm.sessionmaker') as mock_session, \
         patch.object(MSSQLConnector, '_connect', return_value='result'):
        connector = MSSQLConnector(config)
        connector._connect()

        mock_connection = mock_session.return_value.__enter__.return_value
        mock_connection.execute.return_value = "result"

        result = connector.execute_query("SELECT * FROM valid_table")

        assert result == "result"
