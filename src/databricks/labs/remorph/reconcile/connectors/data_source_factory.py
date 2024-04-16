from databricks.labs.blueprint.entrypoint import get_logger
from databricks.sdk import WorkspaceClient  # pylint: disable-next=wrong-import-order
from pyspark.sql import SparkSession

# pylint: disable-next=ungrouped-imports
from databricks.labs.remorph.reconcile.connectors.data_source import DataSource
from databricks.labs.remorph.reconcile.connectors.databricks import DatabricksDataSource
from databricks.labs.remorph.reconcile.connectors.oracle import OracleDataSource
from databricks.labs.remorph.reconcile.connectors.snowflake import SnowflakeDataSource
from databricks.labs.remorph.reconcile.constants import SourceType

logger = get_logger(__file__)


class DataSourceFactory:
    @staticmethod
    def get_data_source(
        engine: str,
        spark: SparkSession,
        ws: WorkspaceClient,
        scope: str,
    ) -> DataSource:
        match engine.lower():
            case SourceType.SNOWFLAKE.value:
                return SnowflakeDataSource(engine, spark, ws, scope)
            case SourceType.ORACLE.value:
                return OracleDataSource(engine, spark, ws, scope)
            case SourceType.DATABRICKS.value:
                return DatabricksDataSource(engine, spark, ws, scope)
            case _:
                raise ValueError(f"Unsupported engine: {engine}")
