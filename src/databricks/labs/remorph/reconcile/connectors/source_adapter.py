from pyspark.sql import SparkSession
from sqlglot import Dialects

from databricks.labs.remorph.config import SQLGLOT_DIALECTS
from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
from databricks.labs.remorph.reconcile.connectors.databricks import DatabricksDataSource
from databricks.labs.remorph.reconcile.connectors.oracle import OracleDataSource
from databricks.labs.remorph.reconcile.connectors.snowflake import SnowflakeDataSource
from databricks.sdk import WorkspaceClient


class DataSourceAdapter:
    @staticmethod
    def create_adapter(engine: Dialects, spark: SparkSession, ws: WorkspaceClient, secret_scope: str) -> DataSource:
        if engine == SQLGLOT_DIALECTS.get("snowflake"):
            return SnowflakeDataSource(engine, spark, ws, secret_scope)
        if engine == SQLGLOT_DIALECTS.get("oracle"):
            return OracleDataSource(engine, spark, ws, secret_scope)
        if engine == SQLGLOT_DIALECTS.get("databricks"):
            return DatabricksDataSource(engine, spark, ws, secret_scope)
        raise ValueError(f"Unsupported source type --> {engine}")
