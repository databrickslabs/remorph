import re
from unittest.mock import MagicMock, create_autospec

import pytest
from databricks.sdk import WorkspaceClient
from pyspark.errors import PySparkException

from databricks.labs.remorph.reconcile.connectors.snowflake import SnowflakeDataSource
from databricks.labs.remorph.reconcile.constants import SourceDriver
from databricks.labs.remorph.reconcile.recon_config import JdbcReaderOptions, Table


def initial_setup():
    pyspark_sql_session = MagicMock()
    spark = pyspark_sql_session.SparkSession.builder.getOrCreate()

    # Define the source, workspace, and scope
    source = "snowflake"
    ws = create_autospec(WorkspaceClient)
    scope = "scope"
    return source, spark, ws, scope


def test_get_jdbc_url():
    # initial setup
    source, spark, ws, scope = initial_setup()
    # Mocking get secret method to return the required values
    ws.secrets.get_secret = MagicMock()
    ws.secrets.get_secret.side_effect = lambda scope, secret_name: {
        'snowflake_account': 'my_account',
        'snowflake_sfUser': 'my_user',
        'snowflake_sfPassword': 'my_password',
        'snowflake_sfDatabase': 'my_database',
        'snowflake_sfSchema': 'my_schema',
        'snowflake_sfWarehouse': 'my_warehouse',
        'snowflake_sfRole': 'my_role',
        'snowflake_sfUrl': 'my_url',
    }[secret_name]
    # create object for SnowflakeDataSource
    ds = SnowflakeDataSource(source, spark, ws, scope)
    url = ds.get_jdbc_url
    # Assert that the URL is generated correctly
    assert url == (
        "jdbc:snowflake://my_account.snowflakecomputing.com"
        "/?user=my_user&password=my_password"
        "&db=my_database&schema=my_schema"
        "&warehouse=my_warehouse&role=my_role"
    )


def test_read_data_with_out_options():
    # initial setup
    source, spark, ws, scope = initial_setup()
    # Mocking get secret method to return the required values
    ws.secrets.get_secret = MagicMock()
    ws.secrets.get_secret.side_effect = lambda scope, secret_name: {
        'snowflake_account': 'my_account',
        'snowflake_sfUser': 'my_user',
        'snowflake_sfPassword': 'my_password',
        'snowflake_sfDatabase': 'my_database',
        'snowflake_sfSchema': 'my_schema',
        'snowflake_sfWarehouse': 'my_warehouse',
        'snowflake_sfRole': 'my_role',
        'snowflake_sfUrl': 'my_url',
    }[secret_name]

    # create object for SnowflakeDataSource
    ds = SnowflakeDataSource(source, spark, ws, scope)
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
    ds.read_data("catalog", "schema", "select 1 from dual", table_conf.jdbc_reader_options)

    # spark assertions
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


def test_read_data_with_options():
    # initial setup
    source, spark, ws, scope = initial_setup()
    # Mocking get secret method to return the required values
    ws.secrets.get_secret = MagicMock()
    ws.secrets.get_secret.side_effect = lambda scope, secret_name: {
        'snowflake_account': 'my_account',
        'snowflake_sfUser': 'my_user',
        'snowflake_sfPassword': 'my_password',
        'snowflake_sfDatabase': 'my_database',
        'snowflake_sfSchema': 'my_schema',
        'snowflake_sfWarehouse': 'my_warehouse',
        'snowflake_sfRole': 'my_role',
        'snowflake_sfUrl': 'my_url',
    }[secret_name]

    # create object for SnowflakeDataSource
    ds = SnowflakeDataSource(source, spark, ws, scope)
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
    ds.read_data("catalog", "schema", "select 1 from dual", table_conf.jdbc_reader_options)

    # spark assertions
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


def test_get_schema():
    # initial setup
    source, spark, ws, scope = initial_setup()
    # Mocking get secret method to return the required values
    ws.secrets.get_secret = MagicMock()
    ws.secrets.get_secret.side_effect = lambda scope, secret_name: {
        'snowflake_account': 'my_account',
        'snowflake_sfUser': 'my_user',
        'snowflake_sfPassword': 'my_password',
        'snowflake_sfDatabase': 'my_database',
        'snowflake_sfSchema': 'my_schema',
        'snowflake_sfWarehouse': 'my_warehouse',
        'snowflake_sfRole': 'my_role',
        'snowflake_sfUrl': 'my_url',
    }[secret_name]

    # create object for SnowflakeDataSource
    ds = SnowflakeDataSource(source, spark, ws, scope)
    # call test method
    ds.get_schema("catalog", "schema", "supplier")
    # spark assertions
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


def test_get_schema_query():
    # initial setup
    source, spark, ws, scope = initial_setup()
    # create object for SnowflakeDataSource
    ds = SnowflakeDataSource(source, spark, ws, scope)
    schema = ds.get_schema_query("catalog", "schema", "supplier")
    assert schema == re.sub(
        r'\s+',
        ' ',
        """select column_name, case when numeric_precision is not null and numeric_scale is not null then
        concat(data_type, '(', numeric_precision, ',' , numeric_scale, ')') when lower(data_type) = 'text' then
        concat('varchar', '(', CHARACTER_MAXIMUM_LENGTH, ')')  else data_type end as data_type from
        catalog.INFORMATION_SCHEMA.COLUMNS where lower(table_name)='supplier' and lower(table_schema) = 'schema' order by ordinal_position""",
    )


def test_read_data_exception_handling():
    # initial setup
    source, spark, ws, scope = initial_setup()
    ds = SnowflakeDataSource(source, spark, ws, scope)
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

    spark.read.format().option().options().load.side_effect = PySparkException("Test Exception")

    # Call the read_data method with the Tables configuration and assert that a PySparkException is raised
    with pytest.raises(
        PySparkException,
        match="An error occurred while fetching Snowflake Data using the following "
        "select 1 from dual in SnowflakeDataSource : Test Exception",
    ):
        ds.read_data("catalog", "schema", "select 1 from dual", table_conf.jdbc_reader_options)


def test_get_schema_exception_handling():
    # initial setup
    source, spark, ws, scope = initial_setup()
    ds = SnowflakeDataSource(source, spark, ws, scope)

    spark.read.format().option().options().load.side_effect = PySparkException("Test Exception")

    # Call the get_schema method with predefined table, schema, and catalog names and assert that a PySparkException
    # is raised
    with pytest.raises(
        PySparkException,
        match="An error occurred while fetching Snowflake Schema using the following "
        "supplier in SnowflakeDataSource: Test Exception",
    ):
        ds.get_schema("catalog", "schema", "supplier")
