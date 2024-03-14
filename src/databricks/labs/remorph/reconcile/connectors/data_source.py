from abc import ABC, abstractmethod

from pyspark.sql import DataFrame, SparkSession

from databricks.labs.remorph.reconcile.recon_config import (
    JdbcReaderOptions,
    Schema,
    Tables,
)


class DataSource(ABC):

    # TODO need to remove connection_params
    def __init__(self, source: str, spark: SparkSession, connection_params: dict[str, str]):
        self.source = source
        self.spark = spark
        self.connection_params = connection_params

    # TODO change the secret retrieval to secrets
    @property
    def get_jdbc_url(self) -> str:
        return (
            f"jdbc:{self.source}:thin:{self.connection_params['user']}"
            f"/{self.connection_params['password']}@//{self.connection_params['host']}"
            f":{self.connection_params['port']}/{self.connection_params['database']}"
        )

    @abstractmethod
    def read_data(self, schema_name: str, catalog_name: str, table_or_query: str, table_conf: Tables) -> DataFrame:
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
        }
