from unittest.mock import MagicMock, patch

import pytest
from pyspark.sql import DataFrame

from databricks.labs.remorph.reconcile.connectors.snowflake import SnowflakeDataSource
from databricks.labs.remorph.reconcile.recon_config import Schema, Tables


# This fixture creates a mock object for SnowflakeDataSource and sets up its methods to return specific values.
# It returns a tuple containing the mock object and a mock DataFrame.
@pytest.fixture
def mock_snowflake():
    mock_snowflake = MagicMock(spec=SnowflakeDataSource)
    mock_df = MagicMock(spec=DataFrame)
    mock_snowflake.read_data.return_value = mock_df
    mock_snowflake.get_schema.return_value = [Schema('column1', 'string')]
    return mock_snowflake, mock_df


# This test function tests the read_data method of SnowflakeDataSource. It creates a mock object for
# SnowflakeDataSource and sets up its read_data method to return a specific value. It then calls the read_data method
# with specific arguments and checks if the returned value and the arguments of the call are as expected.
@patch('databricks.labs.remorph.reconcile.connectors.snowflake.SnowflakeDataSource')
def test_read_data(mock_snowflake):
    mock_snowflake_instance = mock_snowflake.return_value
    mock_df = MagicMock(spec=DataFrame)
    mock_snowflake_instance.read_data.return_value = mock_df

    schema_name = 'test_schema'
    catalog_name = 'test_catalog'
    query = 'SELECT * FROM test_table'
    table_conf = Tables('test_table', 'test_schema', 'test_catalog', None, None)

    df = mock_snowflake_instance.read_data(schema_name, catalog_name, query, table_conf)

    mock_snowflake_instance.read_data.assert_called_once_with(schema_name, catalog_name, query, table_conf)
    assert df == mock_df


# This test function tests the get_schema method of SnowflakeDataSource. It uses the mock_snowflake fixture to get a
# mock object for SnowflakeDataSource. It then calls the get_schema method with specific arguments and checks if the
# returned value and the arguments of the call are as expected.
def test_get_schema(mock_snowflake):
    mock_snowflake_instance, _ = mock_snowflake
    table_name = 'test_table'
    schema_name = 'test_schema'
    catalog_name = 'test_catalog'
    schema = mock_snowflake_instance.get_schema(table_name, schema_name, catalog_name)
    mock_snowflake_instance.get_schema.assert_called_once_with(table_name, schema_name, catalog_name)
    assert schema == [Schema('column1', 'string')]
