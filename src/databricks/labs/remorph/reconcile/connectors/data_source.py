from abc import ABC, abstractmethod

from pyspark.sql import DataFrame


class DataSource(ABC):
    @abstractmethod
    def read_data(self, table_name: str, schema_name: str, catalog_name: str, query: str) -> DataFrame:
        return NotImplemented

    @abstractmethod
    def get_schema(self, table_name: str, schema_name: str, catalog_name: str) -> dict[str, str]:
        return NotImplemented
