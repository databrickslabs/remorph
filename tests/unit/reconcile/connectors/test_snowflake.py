from unittest.mock import MagicMock

import pytest
from pyspark.errors import PySparkException

from databricks.labs.remorph.reconcile.connectors.snowflake import SnowflakeDataSource
from databricks.labs.remorph.reconcile.recon_config import JdbcReaderOptions, Tables


@pytest.fixture
def snowflake_data_source():
    """
    This fixture creates a mock instance of the SnowflakeDataSource class for testing purposes.

    The SnowflakeDataSource instance is created with a mock SparkSession and predefined source, workspace, and scope.
    The _get_secrets method of the instance is also mocked to return predefined secrets based on the secret name.

    Returns:
        SnowflakeDataSource: A mock instance of the SnowflakeDataSource class.
    """

    # Create a mock SparkSession
    pyspark_sql_session = MagicMock()
    spark = pyspark_sql_session.SparkSession.builder.getOrCreate()

    # Define the source, workspace, and scope
    source = "snowflake"
    ws = "ws"
    scope = "scope"

    # Create a mock instance of SnowflakeDataSource
    SnowflakeDataSource_ = SnowflakeDataSource(source, spark, ws, scope)

    # Mock the _get_secrets method to return predefined secrets
    SnowflakeDataSource_._get_secrets = MagicMock()
    SnowflakeDataSource_._get_secrets.side_effect = lambda secret_name: {
        'account': 'my_account',
        'sfUser': 'my_user',
        'sfPassword': 'my_password',
        'sfDatabase': 'my_database',
        'sfSchema': 'my_schema',
        'sfWarehouse': 'my_warehouse',
        'sfRole': 'my_role',
        'sfUrl': 'my_url',
    }[secret_name]

    # Return the mock instance
    return SnowflakeDataSource_


def test_get_jdbc_url(snowflake_data_source):
    """
    This test function verifies the correctness of the get_jdbc_url method of the SnowflakeDataSource class.

    The function retrieves the JDBC URL from the snowflake_data_source fixture and asserts that it matches the expected format.

    Args:
        snowflake_data_source (fixture): A pytest fixture that returns a mock instance of the SnowflakeDataSource class.

    Raises:
        AssertionError: If the generated JDBC URL does not match the expected format.
    """

    # Call the get_jdbc_url method
    url = snowflake_data_source.get_jdbc_url

    # Assert that the URL is generated correctly
    assert url == (
        "jdbc:snowflake://my_account.snowflakecomputing.com"
        "/?user=my_user&password=my_password"
        "&db=my_database&schema=my_schema"
        "&warehouse=my_warehouse&role=my_role"
    )


def test_read_data_with_out_options(snowflake_data_source):
    """
    This test function verifies the behavior of the read_data method of the SnowflakeDataSource class when no JDBC reader options are provided.

    The function creates a Tables configuration object with no JDBC reader options and calls the read_data method with this configuration.
    It then asserts that the reader method of the SnowflakeDataSource instance was called with the correct SQL query.

    Args:
        snowflake_data_source (fixture): A pytest fixture that returns a mock instance of the SnowflakeDataSource class.

    Raises:
        AssertionError: If the reader method was not called with the correct SQL query.
    """

    # Create a Tables configuration object with no JDBC reader options
    table_conf = Tables(
        source_name="supplier",
        target_name="supplier",
        jdbc_reader_options=None,
        join_columns=None,
        select_columns=None,
        drop_columns=None,
        column_mapping=None,
        transformations=None,
        thresholds=None,
        filters=None,
    )

    # Mock the reader method of the SnowflakeDataSource instance
    snowflake_data_source.reader = MagicMock()

    # Call the read_data method with the Tables configuration
    snowflake_data_source.read_data("schema", "catalog", "select 1 from dual", table_conf)

    # Assert that the reader method was called with the correct SQL query
    snowflake_data_source.reader.assert_called_once_with("select 1 from dual")


def test_read_data_with_options(snowflake_data_source):
    """
    This test function verifies the behavior of the read_data method of the SnowflakeDataSource class when JDBC reader options are provided.

    The function creates a Tables configuration object with JDBC reader options and calls the read_data method with this configuration.
    It then asserts that the _get_jdbc_reader and _get_jdbc_reader_options methods of the SnowflakeDataSource instance were called with the correct arguments.

    Args:
        snowflake_data_source (fixture): A pytest fixture that returns a mock instance of the SnowflakeDataSource class.

    Raises:
        AssertionError: If the _get_jdbc_reader or _get_jdbc_reader_options methods were not called with the correct arguments.
    """

    # Create a Tables configuration object with JDBC reader options
    table_conf = Tables(
        source_name="supplier",
        target_name="supplier",
        jdbc_reader_options=JdbcReaderOptions(
            number_partitions=100, partition_column="s_nationkey", lower_bound="0", upper_bound="100"
        ),
        join_columns=None,
        select_columns=None,
        drop_columns=None,
        column_mapping=None,
        transformations=None,
        thresholds=None,
        filters=None,
    )

    # Mock the JDBC reader object and the _get_jdbc_reader_options method
    snowflake_data_source._get_jdbc_reader = MagicMock()
    snowflake_data_source._get_jdbc_reader_options = MagicMock()

    # Call the read_data method with the Tables configuration
    snowflake_data_source.read_data("schema", "catalog", "select 1 from dual", table_conf)

    # Assert that the _get_jdbc_reader and _get_jdbc_reader_options methods were called with the correct arguments
    snowflake_data_source._get_jdbc_reader.assert_called_once_with(
        "select 1 from dual", snowflake_data_source.get_jdbc_url, 'net.snowflake.client.jdbc.SnowflakeDriver'
    )
    snowflake_data_source._get_jdbc_reader_options.assert_called_once_with(table_conf.jdbc_reader_options)


def test_get_schema(snowflake_data_source):
    """
    This test function verifies the behavior of the get_schema method of the SnowflakeDataSource class.

    The function calls the get_schema method with predefined table, schema, and catalog names and does not assert any conditions.

    Args:
        snowflake_data_source (fixture): A pytest fixture that returns a mock instance of the SnowflakeDataSource class.
    """

    snowflake_data_source.get_schema("supplier", "schema", "catalog")


def test_get_schema_query(snowflake_data_source):
    """
    This test function verifies the behavior of the _get_schema_query method of the SnowflakeDataSource class.

    The function calls the _get_schema_query method with predefined table, schema, and catalog names and asserts that the returned SQL query matches the expected format.

    Args:
        snowflake_data_source (fixture): A pytest fixture that returns a mock instance of the SnowflakeDataSource class.

    Raises:
        AssertionError: If the returned SQL query does not match the expected format.
    """

    schema = snowflake_data_source._get_schema_query("supplier", "schema", "catalog")
    assert (
        schema
        == """ select column_name, case when numeric_precision is not null and numeric_scale is not null then concat(data_type, '(', numeric_precision, ',' , numeric_scale, ')') 
        when lower(data_type) = 'text' then concat('varchar', '(', CHARACTER_MAXIMUM_LENGTH, ')')  else data_type end as data_type from 
        catalog.INFORMATION_SCHEMA.COLUMNS where lower(table_name)='supplier' and lower(table_schema) = 'schema' order by ordinal_position
        """.strip()
    )


def test_read_data_exception_handling(snowflake_data_source):
    """
    This test function verifies the exception handling of the read_data method of the SnowflakeDataSource class.

    The function creates a Tables configuration object and calls the read_data method with this configuration.
    It then asserts that a PySparkException is raised.

    Args:
        snowflake_data_source (fixture): A pytest fixture that returns a mock instance of the SnowflakeDataSource class.

    Raises:
        PySparkException: If the read_data method raises a PySparkException.
    """

    # Create a Tables configuration object
    table_conf = Tables(
        source_name="supplier",
        target_name="supplier",
        jdbc_reader_options=None,
        join_columns=None,
        select_columns=None,
        drop_columns=None,
        column_mapping=None,
        transformations=None,
        thresholds=None,
        filters=None,
    )

    # Mock the reader method of the SnowflakeDataSource instance to raise a PySparkException
    snowflake_data_source.reader = MagicMock(side_effect=PySparkException("Test Exception"))

    # Call the read_data method with the Tables configuration and assert that a PySparkException is raised
    with pytest.raises(PySparkException):
        snowflake_data_source.read_data("schema", "catalog", "select 1 from dual", table_conf)


def test_get_schema_exception_handling(snowflake_data_source):
    """
    This test function verifies the exception handling of the get_schema method of the SnowflakeDataSource class.

    The function sets the reader method of the SnowflakeDataSource instance to raise a PySparkException when called.
    It then calls the get_schema method with predefined table, schema, and catalog names and asserts that a PySparkException is raised.

    Args:
        snowflake_data_source (fixture): A pytest fixture that returns a mock instance of the SnowflakeDataSource class.

    Raises:
        PySparkException: If the get_schema method raises a PySparkException.
    """

    # Mock the reader method of the SnowflakeDataSource instance to raise a PySparkException
    snowflake_data_source.reader = MagicMock(side_effect=PySparkException("Test Exception"))

    # Call the get_schema method with predefined table, schema, and catalog names and assert that a PySparkException is raised
    with pytest.raises(PySparkException):
        snowflake_data_source.get_schema("table_name", "schema_name", "catalog_name")
