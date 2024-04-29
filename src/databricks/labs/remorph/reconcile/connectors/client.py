import logging

from pyspark.sql import SparkSession

from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
from databricks.labs.remorph.reconcile.connectors.databricks import DatabricksDataSource
from databricks.labs.remorph.reconcile.connectors.oracle import OracleDataSource
from databricks.labs.remorph.reconcile.connectors.snowflake import SnowflakeDataSource
from databricks.labs.remorph.reconcile.constants import SourceType
from databricks.sdk import WorkspaceClient

logger = logging.getLogger(__name__)


def get_data_source(
    engine: str,
    spark: SparkSession,
    ws: WorkspaceClient,
    scope: str,
) -> DataSource:
    logger.debug(f"Creating DataSource for `{engine.lower()}`")
    match engine.lower():
        case SourceType.SNOWFLAKE.value:
            return SnowflakeDataSource(spark, ws, scope)
        case SourceType.ORACLE.value:
            return OracleDataSource(spark, ws, scope)
        case SourceType.DATABRICKS.value:
            return DatabricksDataSource(spark, ws, scope)
        case _:
            raise ValueError(f"Unsupported engine: {engine}")
