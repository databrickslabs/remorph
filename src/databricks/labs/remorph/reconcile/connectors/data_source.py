from abc import ABC, abstractmethod

from databricks.sdk import WorkspaceClient  # pylint: disable-next=wrong-import-order
from pyspark.sql import DataFrame, SparkSession

from databricks.labs.remorph.reconcile.recon_config import (  # pylint: disable=ungrouped-imports
    JdbcReaderOptions,
    Schema,
    Tables,
)


class DataSource(ABC):

    # TODO need to remove connection_params
    def __init__(self, source: str, spark: SparkSession, ws: WorkspaceClient, scope: str):
        self.source = source
        self.spark = spark
        self.ws = ws
        self.scope = scope

    @abstractmethod
    def read_data(self, schema_name: str, catalog_name: str, query: str, table_conf: Tables) -> DataFrame:
        return NotImplemented

    @abstractmethod
    def get_schema(self, table_name: str, schema_name: str, catalog_name: str) -> list[Schema]:
        return NotImplemented

    def _get_jdbc_reader(self, query, jdbc_url, driver):
        return (
            self.spark.read.format("jdbc")
            .option("url", jdbc_url)
            .option("driver", driver)
            .option("dbtable", f"({query}) tmp")
        )

    @staticmethod
    def _get_jdbc_reader_options(jdbc_reader_options: JdbcReaderOptions):
        return {
            "numPartitions": jdbc_reader_options.number_partitions,
            "partitionColumn": jdbc_reader_options.partition_column,
            "lowerBound": jdbc_reader_options.lower_bound,
            "upperBound": jdbc_reader_options.upper_bound,
            "fetchsize": jdbc_reader_options.fetch_size,
        }

    def _get_secrets(self, key_name):
        key = self.source + '_' + key_name
        return self.ws.secrets.get_secret(self.scope, key)
