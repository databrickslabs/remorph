from unittest.mock import MagicMock, create_autospec

import pytest
from pyspark.errors import PySparkException

from databricks.labs.remorph.reconcile.connectors.oracle import OracleDataSource
from databricks.sdk import WorkspaceClient

from databricks.labs.remorph.reconcile.recon_config import JdbcReaderOptions


def initial_setup():
    pyspark_sql_session = MagicMock()
    spark = pyspark_sql_session.SparkSession.builder.getOrCreate()

    # Define the source, workspace, and scope
    engine = "oracle"
    ws = create_autospec(WorkspaceClient)
    scope = "scope"
    return engine, spark, ws, scope


def test_get_jdbc_url():
    # initial setup
    engine, spark, ws, scope = initial_setup()
    # Mocking get secret method to return the required values
    ws.secrets.get_secret = MagicMock()
    ws.secrets.get_secret.side_effect = lambda scope, secret_name: {
        'oracle_user': 'my_user',
        'oracle_password': 'my_password',
        'oracle_host': 'my_warehouse',
        'oracle_port': '400',
        'oracle_database': 'my_database',
    }[secret_name]
    # create object for SnowflakeDataSource
    ds = OracleDataSource(engine, spark, ws, scope)
    url = ds.get_jdbc_url
    # Assert that the URL is generated correctly
    assert url == ("jdbc:oracle:thin:my_user/my_password@//my_warehouse:400/my_database")


def test_get_schema():
    # initial setup
    engine, spark, ws, scope = initial_setup()
    # Mocking get secret method to return the required values
    ws.secrets.get_secret = MagicMock()
    ws.secrets.get_secret.side_effect = lambda scope, secret_name: {
        'oracle_user': 'my_user',
        'oracle_password': 'my_password',
        'oracle_host': 'my_warehouse',
        'oracle_port': '400',
        'oracle_database': 'my_database',
    }[secret_name]

    # create object for SnowflakeDataSource
    ds = OracleDataSource(engine, spark, ws, scope)
    # call test method
    ds.get_schema("catalog", "schema", "supplier")
    # spark assertions
    spark.read.format.assert_called_with("jdbc")
    spark.read.format().option.assert_called_with(
        "url",
        "jdbc:oracle:thin:my_user/my_password@//my_warehouse:400/my_database",
    )


def test_read_data():
    # initial setup
    engine, spark, ws, scope = initial_setup()
    # Mocking get secret method to return the required values
    ws.secrets.get_secret = MagicMock()
    ws.secrets.get_secret.side_effect = lambda scope, secret_name: {
        'oracle_user': 'my_user',
        'oracle_password': 'my_password',
        'oracle_host': 'my_warehouse',
        'oracle_port': '400',
        'oracle_database': 'my_database',
    }[secret_name]

    # create object for OracleDataSource
    ds = OracleDataSource(engine, spark, ws, scope)

    options = JdbcReaderOptions(
        number_partitions=1, partition_column="id", lower_bound="1", upper_bound="100", fetch_size=1000
    )

    # call test method
    ds.read_data("catalog", "schema", "select 1 from dual", options)

    # spark assertions
    spark.read.format.assert_called_with("jdbc")
    spark.read.format().option.assert_called_with(
        "url",
        "jdbc:oracle:thin:my_user/my_password@//my_warehouse:400/my_database",
    )
    spark.read.format().option.assert_called_with(
        'url', 'jdbc:oracle:thin:my_user/my_password@//my_warehouse:400/my_database'
    )


def test_read_data_exception_handling():
    # initial setup
    engine, spark, ws, scope = initial_setup()
    # Mocking get secret method to return the required values
    ws.secrets.get_secret = MagicMock()
    ws.secrets.get_secret.side_effect = lambda scope, secret_name: {
        'oracle_user': 'my_user',
        'oracle_password': 'my_password',
        'oracle_host': 'my_warehouse',
        'oracle_port': '400',
        'oracle_database': 'my_database',
    }[secret_name]

    # create object for OracleDataSource
    ds = OracleDataSource(engine, spark, ws, scope)

    options = JdbcReaderOptions(
        number_partitions=1, partition_column="id", lower_bound="1", upper_bound="100", fetch_size=1000
    )

    ds.reader(query="SELECT 1 FROM dual").options().load.side_effect = PySparkException("Test Exception")

    # Call the read_data method with the Tables configuration and assert that a PySparkException is raised
    with pytest.raises(
        PySparkException,
        match="An error occurred while fetching Oracle Data using the following "
        "select 1 from dual in OracleDataSource : Test Exception",
    ):
        ds.read_data("catalog", "schema", "select 1 from dual", options)


def test_get_schema_exception_handling():
    # initial setup
    engine, spark, ws, scope = initial_setup()
    # Mocking get secret method to return the required values
    ws.secrets.get_secret = MagicMock()
    ws.secrets.get_secret.side_effect = lambda scope, secret_name: {
        'oracle_user': 'my_user',
        'oracle_password': 'my_password',
        'oracle_host': 'my_warehouse',
        'oracle_port': '400',
        'oracle_database': 'my_database',
    }[secret_name]

    # create object for OracleDataSource
    ds = OracleDataSource(engine, spark, ws, scope)

    ds.reader(query="SELECT 1 FROM dual").load.side_effect = PySparkException("Test Exception")

    with pytest.raises(
        PySparkException,
        match="An error occurred while fetching Oracle Schema using the following "
        "supplier in OracleDataSource: Test Exception",
    ):
        ds.get_schema("catalog", "schema", "supplier")
