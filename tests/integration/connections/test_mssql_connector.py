from databricks.labs.remorph.connections.database_manager import MSSQLConnector


def test_mssql_connector_connection(db_manager):
    assert isinstance(db_manager.connector, MSSQLConnector)


def test_mssql_connector_execute_query(db_manager):
    # Test executing a query
    query = "SELECT 101 AS test_column"
    result = db_manager.execute_query(query)
    row = result.fetchone()
    assert row[0] == 101


def test_connection_test(db_manager):
    assert db_manager.check_connection()
