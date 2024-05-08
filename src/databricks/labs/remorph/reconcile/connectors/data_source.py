import re
from abc import ABC, abstractmethod

from pyspark.sql import DataFrame, SparkSession

from databricks.labs.remorph.reconcile.recon_config import JdbcReaderOptions, Schema
from databricks.sdk import WorkspaceClient


class DataSource(ABC):
    # TODO need to remove connection_params
    def __init__(
            self,
            engine: str,
            spark: SparkSession,
            ws: WorkspaceClient,
            scope: str,
            catalog: str,
            schema: str
    ):
        self._engine = engine
        self.spark = spark
        self._ws = ws
        self._scope = scope
        self._catalog = catalog
        self._schema = schema

    @property
    def engine(self):
        return self._engine

    @property
    def ws(self):
        return self._ws

    @property
    def scope(self):
        return self._scope

    @property
    def catalog(self):
        return self._catalog

    @property
    def schema(self):
        return self._schema

    @abstractmethod
    def read_data(self, query: str, options: JdbcReaderOptions) -> DataFrame:
        return NotImplemented

    @abstractmethod
    def get_schema(self, table: str) -> list[Schema]:
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
        return self.ws.secrets.get_secret(self.scope, key)

    @staticmethod
    def _get_table_or_query(catalog: str, schema: str, query: str) -> str:
        if re.search('select', query, re.IGNORECASE):
            return query.format(catalog_name=catalog, schema_name=schema)
        if catalog and catalog != "hive_metastore":
            return f"select * from {catalog}.{schema}.{query}"
        return f"select * from {schema}.{query}"
