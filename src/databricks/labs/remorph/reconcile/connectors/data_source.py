from abc import ABC, abstractmethod

from pyspark.sql import DataFrame

from databricks.labs.remorph.reconcile.recon_config import JdbcReaderOptions, Schema


class DataSource(ABC):

    @abstractmethod
    def read_query_data(self, catalog: str, schema: str, query: str, options: JdbcReaderOptions | None) -> DataFrame:
        return NotImplemented

    @abstractmethod
    def get_schema(self, catalog: str, schema: str, table: str) -> list[Schema]:
        return NotImplemented
