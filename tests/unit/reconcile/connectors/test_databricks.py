import re
from unittest.mock import MagicMock, create_autospec

from databricks.labs.remorph.config import get_dialect
from databricks.labs.remorph.reconcile.connectors.databricks import DatabricksDataSource
from databricks.sdk import WorkspaceClient


def initial_setup():
    pyspark_sql_session = MagicMock()
    spark = pyspark_sql_session.SparkSession.builder.getOrCreate()

    # Define the source, workspace, and scope
    engine = get_dialect("databricks")
    ws = create_autospec(WorkspaceClient)
    scope = "scope"
    return engine, spark, ws, scope


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


def test_read_data_from_uc():
    # initial setup
    engine, spark, ws, scope = initial_setup()

    # create object for DatabricksDataSource
    dd = DatabricksDataSource(engine, spark, ws, scope)

    # Test with query
    dd.read_data("org", "data", "employee", "select id as id, name as name from :tbl", None)
    spark.sql.assert_called_with("select id as id, name as name from org.data.employee")


def test_read_data_from_hive():
    # initial setup
    engine, spark, ws, scope = initial_setup()

    # create object for DatabricksDataSource
    dd = DatabricksDataSource(engine, spark, ws, scope)

    # Test with query
    dd.read_data("hive_metastore", "data", "employee", "select id as id, name as name from :tbl", None)
    spark.sql.assert_called_with("select id as id, name as name from data.employee")


def test_read_data_exception_handling():
    # initial setup
    engine, spark, ws, scope = initial_setup()

    # create object for DatabricksDataSource
    dd = DatabricksDataSource(engine, spark, ws, scope)
    spark.sql.side_effect = RuntimeError("Test Exception")

    actual = dd.read_data("org", "data", "employee", "select id as id, ename as name from :tbl", None)
    assert actual is None, "the expected value is None"


def test_get_schema_exception_handling():
    # initial setup
    engine, spark, ws, scope = initial_setup()

    # create object for DatabricksDataSource
    dd = DatabricksDataSource(engine, spark, ws, scope)
    spark.sql.side_effect = RuntimeError("Test Exception")
    actual = dd.get_schema("org", "data", "employee")
    assert actual is None, "the expected value is None"
