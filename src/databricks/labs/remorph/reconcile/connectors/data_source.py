import logging
import re
from abc import ABC, abstractmethod

from pyspark.sql import DataFrame, SparkSession

from databricks.labs.remorph.config import TableRecon
from databricks.labs.remorph.reconcile.recon_config import JdbcReaderOptions, Schema
from databricks.sdk import WorkspaceClient

logger = logging.getLogger(__name__)


class DataSource(ABC):
    # TODO need to remove connection_params
    def __init__(
        self,
        spark: SparkSession,
        ws: WorkspaceClient,
        scope: str,
        engine: str = None,
    ):
        self.engine = engine
        self.spark = spark
        self.ws = ws
        self.scope = scope

    @abstractmethod
    def read_data(self, catalog: str, schema: str, query: str, options: JdbcReaderOptions | None) -> DataFrame:
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
        secret = dbutils.secrets.get(scope=self.scope, key=key)
        logger.debug(f"Secret fetched successfully for {key}")
        return secret

    @staticmethod
    def _get_table_or_query(catalog: str, schema: str, query: str) -> str:
        if re.search('select', query, re.IGNORECASE):
            return query.format(catalog_name=catalog, schema_name=schema)
        if catalog and catalog != "hive_metastore":
            return f"select * from {catalog}.{schema}.{query}"
        return f"select * from {schema}.{query}"
