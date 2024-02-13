from abc import ABC, abstractmethod

from databricks.labs.blueprint.entrypoint import get_logger

from databricks.labs.remorph.reconcile.recon_config import Schema, Tables, QueryColumnConfig, \
    QueryColumnWithTransformation

logger = get_logger(__file__)


class SourceQueryBuildAdapter(ABC):

    def __init__(self, source_type: str, table_conf: Tables, schema: list[Schema]):
        self.source_type = source_type
        self.table_conf = table_conf
        self.schema = schema

    @abstractmethod
    def get_select_columns(self) -> QueryColumnConfig:
        pass

    # @abstractmethod
    # def remove_drop_cols_from_sel_cols(self) -> QueryColumnConfig:
    #     pass

    @abstractmethod
    def get_join_columns(self, col_config) -> QueryColumnConfig:
        pass

    @abstractmethod
    def get_jdbc_partition_column(self, col_config) -> QueryColumnConfig:
        pass

    @abstractmethod
    def add_default_transformation_to_cols(self,col_config) -> QueryColumnWithTransformation:
        pass

    @abstractmethod
    def generate_hash_column(self,transformation_config) -> QueryColumnWithTransformation:
        pass

    @abstractmethod
    def generate_hash_algorithm(self,transformation_config) -> QueryColumnWithTransformation:
        pass

    @abstractmethod
    def generate_sql_query(self) -> str:
        pass
