from abc import ABC, abstractmethod

from pyspark.sql import DataFrame, SparkSession

from databricks.labs.remorph.reconcile.constants import Constants
from databricks.labs.remorph.reconcile.recon_config import (
    DatabaseConfig,
    Schema,
    Tables,
    TransformRuleMapping,
)
from typing import List


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
    def generate_hash_column(cls, column_expr: List[str], layer: str) -> str:
        concat_columns = " || ".join(column_expr)
        hash_algo = Constants.hash_algorithm_mapping.get(cls.get_source_type).get(layer)
        return hash_algo.format(concat_columns)

    @abstractmethod
    def extract_data(self, table_conf: Tables, query: str) -> DataFrame:
        pass

    @abstractmethod
    def extract_schema(self, database_conf: DatabaseConfig, table_conf: Tables) -> List[Schema]:
        pass

    @abstractmethod
    def extract_databricks_schema(self, table_conf: Tables, table_name: str) -> List[Schema]:
        try:
            table_name = table_conf.target_name
            databricks_table_schema_df = self.spark.sql(f"describe table {table_name}").where(
                "col_name not like '#%'").distinct()
            databricks_schema = [Schema(field.col_name.lower(), field.data_type.lower()) for field in
                                 databricks_table_schema_df.collect()]
            return databricks_schema
        except Exception as e:
            message = (f"Exception in getting the schema for databricks table in "
                       f"get_databricks_schema() {table_name} --> {e}")
            raise Exception(message)

    @abstractmethod
    def get_column_list_with_transformation(
        self, table_conf: Tables, columns: list[str], layer: str
    ) -> list[TransformRuleMapping]:
        pass
