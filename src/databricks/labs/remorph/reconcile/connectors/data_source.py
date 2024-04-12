import re
from abc import ABC, abstractmethod

from databricks.labs.blueprint.entrypoint import get_logger
from databricks.sdk import WorkspaceClient  # pylint: disable-next=wrong-import-order
from pyspark.sql import DataFrame, SparkSession

# pylint: disable=ungrouped-imports
from databricks.labs.remorph.reconcile.connectors.databricks import DatabricksDataSource
from databricks.labs.remorph.reconcile.connectors.oracle import OracleDataSource
from databricks.labs.remorph.reconcile.connectors.snowflake import SnowflakeDataSource
from databricks.labs.remorph.reconcile.constants import SourceType
from databricks.labs.remorph.reconcile.recon_config import (
    JdbcReaderOptions,
    Schema,
    TableRecon,
)

logger = get_logger(__file__)


class DataSource(ABC):
    # TODO need to remove connection_params
    def __init__(
        self,
        engine: str,
        spark: SparkSession,
        ws: WorkspaceClient,
        scope: str,
    ):
        self.engine = engine
        self.spark = spark
        self.ws = ws
        self.scope = scope

    @abstractmethod
    def read_data(self, catalog: str, schema: str, query: str, options: JdbcReaderOptions) -> DataFrame:
        return NotImplemented

    @abstractmethod
    def get_schema(self, catalog: str, schema: str, table: str) -> list[Schema]:
        return NotImplemented

    @abstractmethod
    def list_tables(
        self,
        catalog: str,
        schema: str,
        include_list: list[str] | None,
        exclude_list: list[str] | None,
    ) -> TableRecon:
        return NotImplemented

    def _get_jdbc_reader(self, query, jdbc_url, driver):
        return (
            self.spark.read.format("jdbc")
            .option("url", jdbc_url)
            .option("driver", driver)
            .option("dbtable", f"({query}) tmp")
        )

    @staticmethod
    def _get_jdbc_reader_options(options: JdbcReaderOptions):
        return {
            "numPartitions": options.number_partitions,
            "partitionColumn": options.partition_column,
            "lowerBound": options.lower_bound,
            "upperBound": options.upper_bound,
            "fetchsize": options.fetch_size,
        }

    def _get_secrets(self, key_name: str):
        key = self.engine + '_' + key_name
        dbutils = self.ws.dbutils
        logger.debug(f"Fetching secret using DBUtils: {key}")
        # ws_secret = self.ws.secrets.get_secret(self.scope, key).value
        # TODO: Use workspace secrets and decode it using dbutils
        secret = dbutils.secrets.get(scope=self.scope, key=key)
        logger.debug(f"Secret fetched successfully `{secret}` for {key}")
        return secret

    @staticmethod
    def _get_table_or_query(catalog: str, schema: str, query: str) -> str:
        if re.search('select', query, re.IGNORECASE):
            return query.format(catalog_name=catalog, schema_name=schema)
        if catalog and catalog != "hive_metastore":
            return f"select * from {catalog}.{schema}.{query}"
        return f"select * from {schema}.{query}"


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
