from abc import ABC, abstractmethod

from pyspark.sql import DataFrame, SparkSession

from databricks.labs.remorph.reconcile.constants import Constants
from databricks.labs.remorph.reconcile.recon_config import (
    DatabaseConfig,
    Schema,
    Tables,
    TransformRuleMapping,
)


class SourceAdapter(ABC):

    def __init__(self, source_type: str, spark: SparkSession, connection_params: dict[str, str]):
        self.source_type = source_type
        self.spark = spark
        self.connection_params = connection_params

    @property
    def get_jdbc_url(self) -> str:
        return (
            f"jdbc:{self.source_type}:thin:{self.connection_params['user']}"
            f"/{self.connection_params['password']}@//{self.connection_params['host']}"
            f":{self.connection_params['port']}/{self.connection_params['database']}"
        )

    @property
    def get_source_type(self) -> str:
        return self.source_type.lower()

    @classmethod
    def generate_hash_column(cls, column_expr: list[str], layer: str) -> str:
        concat_columns = " || ".join(column_expr)
        hash_algo = Constants.hash_algorithm_mapping.get(cls.get_source_type).get(layer)
        return hash_algo.format(concat_columns)

    @abstractmethod
    def extract_data(self, table_conf: Tables, query: str) -> DataFrame:
        pass

    @abstractmethod
    def extract_schema(self, database_conf: DatabaseConfig, table_conf: Tables) -> list[Schema]:
        pass

    @abstractmethod
    def get_column_list_with_transformation(
        self, table_conf: Tables, columns: list[str], layer: str
    ) -> list[TransformRuleMapping]:
        pass
