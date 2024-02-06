import pytest

from databricks.labs.remorph.reconcile.connectors.databricks_connect import (
    DatabricksAdapter,
)
from databricks.labs.remorph.reconcile.connectors.netezza_connect import NetezzaAdapter
from databricks.labs.remorph.reconcile.connectors.oracle_connect import OracleAdapter
from databricks.labs.remorph.reconcile.connectors.snowflake_connect import (
    SnowflakeAdapter,
)
from databricks.labs.remorph.reconcile.connectors.source_connector import (
    SourceAdapterFactory,
)
from databricks.labs.remorph.reconcile.constants import SourceType


def test_source_adapter_factory(mock_spark_session):
    spark = mock_spark_session
    connection_params = {"param1": "value1", "param2": "value2"}

    # Test NetezzaAdapter creation
    adapter = SourceAdapterFactory.create(SourceType.NETEZZA.value, spark, connection_params)
    assert isinstance(adapter, NetezzaAdapter)

    # Test SnowflakeAdapter creation
    adapter = SourceAdapterFactory.create(SourceType.SNOWFLAKE.value, spark, connection_params)
    assert isinstance(adapter, SnowflakeAdapter)

    # Test OracleAdapter creation
    adapter = SourceAdapterFactory.create(SourceType.ORACLE.value, spark, connection_params)
    assert isinstance(adapter, OracleAdapter)

    # Test DatabricksAdapter creation
    adapter = SourceAdapterFactory.create(SourceType.DATABRICKS.value, spark, connection_params)
    assert isinstance(adapter, DatabricksAdapter)

    # Test unsupported source type
    with pytest.raises(ValueError):
        SourceAdapterFactory.create("unsupported_source_type", spark, connection_params)
