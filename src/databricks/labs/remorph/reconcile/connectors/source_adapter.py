from abc import ABC, abstractmethod
from io import StringIO

from databricks.labs.blueprint.entrypoint import get_logger
from pyspark.sql import DataFrame, SparkSession

from databricks.labs.remorph.reconcile.constants import Constants
from databricks.labs.remorph.reconcile.recon_config import (
    ColumnMapping,
    DatabaseConfig,
    Schema,
    Tables,
    Thresholds,
    Transformation,
    TransformRuleMapping,
)

logger = get_logger(__file__)


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
    def query_builder(cls, table_conf: Tables, select_expr: str, join_expr: str | None, layer: str) -> str:
        try:
            sql_query = StringIO()

            sql_query.write("select ")
            sql_query.write(select_expr)
            sql_query.write(f" as {Constants.hash_column_name}")

            if join_expr:
                sql_query.write(" , ")
                sql_query.write(join_expr)

            sql_query.write(" from ")

            # table name
            if layer == "source":
                sql_query.write(table_conf.source_name)
            elif layer == "target":
                sql_query.write(table_conf.target_name)

            # where/filter clause
            if table_conf.filters:
                if layer == "source" and table_conf.filters.source:
                    sql_query.write(" where ")
                    sql_query.write(table_conf.filters.source)
                elif layer == "target" and table_conf.filters.target:
                    sql_query.write(" where ")
                    sql_query.write(table_conf.filters.target)

            final_sql_query = sql_query.getvalue()
            sql_query.close()
            return final_sql_query
        except Exception as e:
            message = f"An error occurred in method generate_full_query: {e!s}"
            logger.error(message)
            raise Exception(message) from e

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
    def extract_databricks_schema(self, table_conf: Tables, table_name: str) -> list[Schema]:
        try:
            table_name = table_conf.target_name
            # [TODO] - We should eventually switch to Unity Catalog
            databricks_table_schema_df = (
                self.spark.sql(f"describe table {table_name}").where("col_name not like '#%'").distinct()
            )
            databricks_schema = [
                Schema(field.col_name.lower(), field.data_type.lower())
                for field in databricks_table_schema_df.collect()
            ]
            return databricks_schema
        except Exception as e:
            message = (
                f"Exception in getting the schema for databricks table in "
                f"get_databricks_schema() {table_name} --> {e}"
            )
            logger.error(message)
            raise Exception(message) from e

    @abstractmethod
    def get_column_list_with_transformation(
        self, table_conf: Tables, columns: list[str], layer: str
    ) -> list[TransformRuleMapping]:
        column_list: list[TransformRuleMapping] = []
        transformation_dict = table_conf.list_to_dict(Transformation, "column_name")
        threshold_dict = table_conf.list_to_dict(Thresholds, "column_name")
        alias_mapping_dict = table_conf.list_to_dict(ColumnMapping, "source_name")

        for column in columns:
            transformation_mapping = TransformRuleMapping("", None, None)
            if alias_mapping_dict is not None and column in alias_mapping_dict.keys():
                transformation_mapping.alias_name = alias_mapping_dict.get(column).target_name
            if transformation_dict is not None and column in transformation_dict.keys():
                match layer:
                    case "source":
                        transformation_mapping.transformation = transformation_dict.get(column).source

                    case "target":
                        transformation_mapping.transformation = transformation_dict.get(column).target
                    case _:
                        print("Invalid layer value only source or target is allowed")
            elif threshold_dict is not None and column in threshold_dict.keys():
                print("columns in threshold will be treated separately")
            else:
                transformation_mapping.column_name = column

            column_list.append(transformation_mapping)

        return column_list
