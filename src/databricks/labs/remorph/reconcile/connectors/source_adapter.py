from pyspark.sql import SparkSession
from sqlglot import Dialect
from sqlglot.dialects import TSQL, Snowflake, Oracle, Databricks

from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
from databricks.labs.remorph.reconcile.connectors.databricks import DatabricksDataSource
from databricks.labs.remorph.reconcile.connectors.oracle import OracleDataSource
from databricks.labs.remorph.reconcile.connectors.snowflake import SnowflakeDataSource
from databricks.labs.remorph.reconcile.connectors.sql_server import SQLServerDataSource
from databricks.sdk import WorkspaceClient


def create_adapter(
    engine: Dialect,
    spark: SparkSession,
    ws: WorkspaceClient,
    secret_scope: str,
) -> DataSource:
    if isinstance(engine, Snowflake):
        return SnowflakeDataSource(engine, spark, ws, secret_scope)
    if isinstance(engine, Oracle):
        return OracleDataSource(engine, spark, ws, secret_scope)
    if isinstance(engine, Databricks):
        return DatabricksDataSource(engine, spark, ws, secret_scope)
    if isinstance(engine, TSQL):
        return SQLServerDataSource(engine, spark, ws, secret_scope)
    raise ValueError(f"Unsupported source type --> {engine}")
