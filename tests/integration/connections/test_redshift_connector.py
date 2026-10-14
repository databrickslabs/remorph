import pytest

from databricks.labs.lakebridge.connections.database_manager import DatabaseConnector, RedshiftConnector

# TODO: re-enable once the CI runners can reach the sandbox Redshift cluster again.
pytestmark = pytest.mark.skip(reason="CI runners currently time out connecting to the sandbox Redshift cluster")


def test_redshift_connector_connection(sandbox_redshift: DatabaseConnector) -> None:
    """Test that the Redshift factory returns a RedshiftConnector."""
    assert isinstance(sandbox_redshift, RedshiftConnector)


def test_redshift_connector_execute_query(sandbox_redshift: DatabaseConnector) -> None:
    """Test executing a query through the Redshift connector."""
    query = "SELECT 101 AS test_column"
    result = sandbox_redshift.fetch(query).rows
    assert result[0][0] == 101


def test_redshift_connection_check(sandbox_redshift: DatabaseConnector) -> None:
    """Test connection check for Redshift."""
    assert sandbox_redshift.health_check()
