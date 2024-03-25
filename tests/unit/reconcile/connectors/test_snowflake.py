import re
from unittest.mock import MagicMock, create_autospec

import pytest
from databricks.sdk import WorkspaceClient
from pyspark.errors import PySparkException

from databricks.labs.remorph.reconcile.connectors.snowflake import SnowflakeDataSource
from databricks.labs.remorph.reconcile.constants import SourceDriver
from databricks.labs.remorph.reconcile.recon_config import JdbcReaderOptions, Table


@pytest.fixture
def snowflake_data_source():
    # Create a mock SparkSession
    pyspark_sql_session = MagicMock()
    spark = pyspark_sql_session.SparkSession.builder.getOrCreate()

    # Define the source, workspace, and scope
    source = "snowflake"
    ws = create_autospec(WorkspaceClient)
    scope = "scope"

    SnowflakeDataSource_ = SnowflakeDataSource(source, spark, ws, scope)
    # Mock the _get_secrets method to return predefined secrets
    SnowflakeDataSource_.get_secrets = MagicMock()
    SnowflakeDataSource_.get_secrets.side_effect = lambda secret_name: {
        'account': 'my_account',
        'sfUser': 'my_user',
        'sfPassword': 'my_password',
        'sfDatabase': 'my_database',
        'sfSchema': 'my_schema',
        'sfWarehouse': 'my_warehouse',
        'sfRole': 'my_role',
        'sfUrl': 'my_url',
    }[secret_name]
    # Create a mock instance of SnowflakeDataSource
    return SnowflakeDataSource_


def test_get_jdbc_url(snowflake_data_source):
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
    table_conf = Table(
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

    # Call the read_data method with the Tables configuration
    snowflake_data_source.read_data("catalog", "schema", "select 1 from dual", table_conf.jdbc_reader_options)

    # spark assertions
    spark = snowflake_data_source.spark
    spark.read.format.assert_called_with("snowflake")
    spark.read.format().option.assert_called_with("dbtable", "(select 1 from dual) as tmp")
    spark.read.format().option().options.assert_called_with(
        sfUrl="my_url",
        sfUser="my_user",
        sfPassword="my_password",
        sfDatabase="my_database",
        sfSchema="my_schema",
        sfWarehouse="my_warehouse",
        sfRole="my_role",
    )
    spark.read.format().option().options().load.assert_called_once()


def test_read_data_with_options(snowflake_data_source):
    """
    This test function verifies the behavior of the read_data method of the SnowflakeDataSource class when JDBC reader options are provided.

    The function creates a Tables configuration object with JDBC reader options and calls the read_data method with this configuration.
    It then asserts that the reader method of the SnowflakeDataSource instance was called with the correct SQL query and options.

    Args:
        snowflake_data_source (fixture): A pytest fixture that returns a mock instance of the SnowflakeDataSource class.

    Raises:
        AssertionError: If the reader method was not called with the correct SQL query and options.
    """

    # Create a Tables configuration object with JDBC reader options
    table_conf = Table(
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

    # Call the read_data method with the Tables configuration
    snowflake_data_source.read_data("catalog", "schema", "select 1 from dual", table_conf.jdbc_reader_options)

    # spark assertions
    spark = snowflake_data_source.spark
    spark.read.format.assert_called_with("jdbc")
    spark.read.format().option.assert_called_with(
        "url",
        "jdbc:snowflake://my_account.snowflakecomputing.com/?user=my_user&password=my_password&db=my_database&schema=my_schema&warehouse=my_warehouse&role=my_role",
    )
    spark.read.format().option().option.assert_called_with("driver", SourceDriver.SNOWFLAKE.value)
    spark.read.format().option().option().option.assert_called_with("dbtable", "(select 1 from dual) tmp")
    spark.read.format().option().option().option().options.assert_called_with(
        numPartitions=100, partitionColumn='s_nationkey', lowerBound='0', upperBound='100', fetchsize=100
    )
    spark.read.format().option().option().option().options().load.assert_called_once()


def test_get_schema(snowflake_data_source):
    snowflake_data_source.get_schema("catalog", "schema", "supplier")
    # spark assertions
    spark = snowflake_data_source.spark
    spark.read.format.assert_called_with("snowflake")
    spark.read.format().option.assert_called_with(
        "dbtable",
        re.sub(
            r'\s+',
            ' ',
            """(select column_name, case when numeric_precision is not null and numeric_scale is not null then 
        concat(data_type, '(', numeric_precision, ',' , numeric_scale, ')') when lower(data_type) = 'text' then 
        concat('varchar', '(', CHARACTER_MAXIMUM_LENGTH, ')')  else data_type end as data_type from 
        catalog.INFORMATION_SCHEMA.COLUMNS where lower(table_name)='supplier' and lower(table_schema) = 'schema' order by ordinal_position) as tmp""",
        ),
    )
    spark.read.format().option().options.assert_called_with(
        sfUrl="my_url",
        sfUser="my_user",
        sfPassword="my_password",
        sfDatabase="my_database",
        sfSchema="my_schema",
        sfWarehouse="my_warehouse",
        sfRole="my_role",
    )
    spark.read.format().option().options().load.assert_called_once()


def test_get_schema_query(snowflake_data_source):
    schema = snowflake_data_source.get_schema_query("catalog", "schema", "supplier")
    assert schema == re.sub(
        r'\s+',
        ' ',
        """select column_name, case when numeric_precision is not null and numeric_scale is not null then 
        concat(data_type, '(', numeric_precision, ',' , numeric_scale, ')') when lower(data_type) = 'text' then 
        concat('varchar', '(', CHARACTER_MAXIMUM_LENGTH, ')')  else data_type end as data_type from 
        catalog.INFORMATION_SCHEMA.COLUMNS where lower(table_name)='supplier' and lower(table_schema) = 'schema' order by ordinal_position""",
    )


def test_read_data_exception_handling(snowflake_data_source):
    # Create a Tables configuration object
    table_conf = Table(
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
        snowflake_data_source.read_data("catalog", "schema", "select 1 from dual", table_conf.jdbc_reader_options)


def test_get_schema_exception_handling(snowflake_data_source):
    # Mock the reader method of the SnowflakeDataSource instance to raise a PySparkException
    snowflake_data_source.reader = MagicMock(side_effect=PySparkException("Test Exception"))

    # Call the get_schema method with predefined table, schema, and catalog names and assert that a PySparkException
    # is raised
    with pytest.raises(PySparkException):
        snowflake_data_source.get_schema("table_name", "schema_name", "catalog_name")
