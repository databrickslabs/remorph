import pytest

from databricks.labs.remorph.connections.database_manager import PostgresConnector
from .helpers import get_db_manager


@pytest.fixture()
def db_manager(mock_credentials):
    return get_db_manager("remorph", "snowflake")


def test_postgres_connector_connection(db_manager):
    assert isinstance(db_manager.connector, PostgresConnector)


def test_postgres_connector_execute_query(db_manager):
    # Execute a sample query
    query = "SELECT 'Fizz buzz"
    result = db_manager.execute_query(query)
    row = result.fetchone()
    assert row[0] == "Fizz buzz"


def test_connection_test(db_manager):
    assert db_manager.check_connection()
