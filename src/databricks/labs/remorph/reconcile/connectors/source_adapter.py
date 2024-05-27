from pyspark.sql import SparkSession
from sqlglot import Dialect

from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
from databricks.labs.remorph.reconcile.connectors.databricks import DatabricksDataSource
from databricks.labs.remorph.reconcile.connectors.oracle import OracleDataSource
from databricks.labs.remorph.reconcile.connectors.snowflake import SnowflakeDataSource
from databricks.labs.remorph.snow.databricks import Databricks
from databricks.labs.remorph.snow.oracle import Oracle
from databricks.labs.remorph.snow.snowflake import Snow
from databricks.sdk import WorkspaceClient


def create_adapter(
    engine: Dialect,
    spark: SparkSession,
    ws: WorkspaceClient,
    secret_scope: str,
) -> DataSource:
    if isinstance(engine, Snow):
        return SnowflakeDataSource(engine, spark, ws, secret_scope)
    if isinstance(engine, Oracle):
        return OracleDataSource(engine, spark, ws, secret_scope)
    if isinstance(engine, Databricks):
        return DatabricksDataSource(engine, spark, ws, secret_scope)
    raise ValueError(f"Unsupported source type --> {engine}")
