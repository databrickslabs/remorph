import re
from unittest.mock import MagicMock, create_autospec

import pytest
from databricks.sdk import WorkspaceClient
from pyspark.errors import PySparkException

from databricks.labs.remorph.reconcile.connectors.databricks import DatabricksDataSource


def initial_setup():
    pyspark_sql_session = MagicMock()
    spark = pyspark_sql_session.SparkSession.builder.getOrCreate()

    # Define the source, workspace, and scope
    engine = "databricks"
    ws = create_autospec(WorkspaceClient)
    scope = "scope"
    return engine, spark, ws, scope


def test_get_schema_query():
    # initial setup
    engine, spark, ws, scope = initial_setup()
    dd = DatabricksDataSource(engine, spark, ws, scope)

    # catalog as catalog
    schema_query = dd.get_schema_query("catalog", "schema", "supplier")
    assert re.sub(r'\s+', ' ', schema_query) == re.sub(
        r'\s+',
        ' ',
        """select lower(column_name) as col_name, full_data_type as data_type from 
                    catalog.information_schema.columns where lower(table_catalog)='catalog' 
                    and lower(table_schema)='schema' and lower(table_name) ='supplier' order by 
                    col_name""",
    )

    # hive_metastore as catalog
    schema_query = dd.get_schema_query("hive_metastore", "schema", "supplier")
    assert re.sub(r'\s+', ' ', schema_query) == re.sub(r'\s+', ' ', """describe table schema.supplier""")


def test_get_schema():
    # initial setup
    engine, spark, ws, scope = initial_setup()

    # catalog as catalog
    dd = DatabricksDataSource(engine, spark, ws, scope)
    dd.get_schema("catalog", "schema", "supplier")
    spark.sql.assert_called_with(
        re.sub(
            r'\s+',
            ' ',
            """select lower(column_name) as col_name, full_data_type as data_type from 
                    catalog.information_schema.columns where lower(table_catalog)='catalog' 
                    and lower(table_schema)='schema' and lower(table_name) ='supplier' order by 
                    col_name""",
        )
    )
    spark.sql().where.assert_called_with("col_name not like '#%'")

    # hive_metastore as catalog
    dd.get_schema("hive_metastore", "schema", "supplier")
    spark.sql.assert_called_with(re.sub(r'\s+', ' ', """describe table schema.supplier"""))
    spark.sql().where.assert_called_with("col_name not like '#%'")


def test_read_data():
    # initial setup
    engine, spark, ws, scope = initial_setup()

    # create object for DatabricksDataSource
    dd = DatabricksDataSource(engine, spark, ws, scope)

    # Test with query
    dd.read_data("catalog", "schema", "select id as id, ename as name from confidential.data.employee", None)
    spark.sql.assert_called_with("select id as id, ename as name from confidential.data.employee")

    # Test with table name
    dd.read_data("catalog", "schema", "employee", None)
    spark.sql.assert_called_with("select * from catalog.schema.employee")


def test_read_data_exception_handling():
    # initial setup
    engine, spark, ws, scope = initial_setup()

    # create object for DatabricksDataSource
    dd = DatabricksDataSource(engine, spark, ws, scope)

    spark.sql.side_effect = PySparkException("Test Exception")

    with pytest.raises(
        PySparkException,
        match="An error occurred while fetching Databricks Data using the "
        "following select id as id, ename as name from "
        "confidential.data.employee in DatabricksDataSource : Test Exception",
    ):
        dd.read_data("catalog", "schema", "select id as id, ename as name from confidential.data.employee", None)


def test_get_schema_exception_handling():
    # initial setup
    engine, spark, ws, scope = initial_setup()

    # create object for DatabricksDataSource
    dd = DatabricksDataSource(engine, spark, ws, scope)
    spark.sql().where.side_effect = PySparkException("Test Exception")
    with pytest.raises(PySparkException, match=".*Test Exception.*"):
        dd.get_schema("catalog", "schema", "supplier")
