import pytest

from databricks.labs.remorph.config import get_dialect
from databricks.labs.remorph.reconcile.connectors.databricks import DatabricksDataSource
from databricks.labs.remorph.reconcile.connectors.oracle import OracleDataSource
from databricks.labs.remorph.reconcile.connectors.snowflake import SnowflakeDataSource
from databricks.labs.remorph.reconcile.connectors.source_adapter import create_adapter


def test_create_adapter_for_snowflake_dialect(mock_spark_session, mock_workspace_client):
    engine = get_dialect("snowflake")
    scope = "scope"

    data_source = create_adapter(engine, mock_spark_session, mock_workspace_client, scope)
    snowflake_data_source = SnowflakeDataSource(engine, mock_spark_session, mock_workspace_client, scope).__class__

    assert isinstance(data_source, snowflake_data_source)


def test_create_adapter_for_oracle_dialect(mock_spark_session, mock_workspace_client):
    engine = get_dialect("oracle")
    scope = "scope"

    data_source = create_adapter(engine, mock_spark_session, mock_workspace_client, scope)
    oracle_data_source = OracleDataSource(engine, mock_spark_session, mock_workspace_client, scope).__class__

    assert isinstance(data_source, oracle_data_source)


def test_create_adapter_for_databricks_dialect(mock_spark_session, mock_workspace_client):
    engine = get_dialect("databricks")
    scope = "scope"

    data_source = create_adapter(engine, mock_spark_session, mock_workspace_client, scope)
    databricks_data_source = DatabricksDataSource(engine, mock_spark_session, mock_workspace_client, scope).__class__

    assert isinstance(data_source, databricks_data_source)


def test_raise_exception_for_unknown_dialect(mock_spark_session, mock_workspace_client):
    engine = get_dialect("trino")
    scope = "scope"

    with pytest.raises(ValueError, match=f"Unsupported source type --> {engine}"):
        create_adapter(engine, mock_spark_session, mock_workspace_client, scope)
