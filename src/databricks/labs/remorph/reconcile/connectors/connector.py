from pyspark.sql import SparkSession

from databricks.labs.remorph.reconcile.connectors.databricks import (
    DatabricksAdapter
)
from databricks.labs.remorph.reconcile.connectors.netezza import NetezzaAdapter
from databricks.labs.remorph.reconcile.connectors.oracle import OracleAdapter
from databricks.labs.remorph.reconcile.connectors.snowflake import SnowflakeAdapter
from databricks.labs.remorph.reconcile.connectors.adapter import SourceAdapter
from databricks.labs.remorph.reconcile.constants import SourceType


class SourceAdapterFactory:
    @staticmethod
    def create(source_type: str, spark: SparkSession, connection_params: dict[str, str]) -> SourceAdapter:

        match source_type.lower():
            case SourceType.NETEZZA.value:
                return NetezzaAdapter(source_type, spark, connection_params)
            case SourceType.SNOWFLAKE.value:
                return SnowflakeAdapter(source_type, spark, connection_params)
            case SourceType.ORACLE.value:
                return OracleAdapter(source_type, spark, connection_params)
            case SourceType.DATABRICKS.value:
                return DatabricksAdapter(source_type, spark, connection_params)
            case _:
                msg = f"Unsupported source type --> {source_type}"
                raise ValueError(msg)