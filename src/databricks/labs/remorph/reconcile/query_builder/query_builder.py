from abc import ABC, abstractmethod
from io import StringIO

from databricks.labs.blueprint.entrypoint import get_logger
from databricks.labs.remorph.reconcile.constants import Constants
from databricks.labs.remorph.reconcile.query_builder.query_configurator import QueryConfig
from databricks.labs.remorph.reconcile.recon_config import Tables, Schema, TransformRuleMapping

logger = get_logger(__file__)


class QueryBuilder(ABC):

    def __init__(self, source_type: str, layer: str, table_conf: Tables, schema: list[Schema]):
        self.source_type = source_type
        self.layer = layer
        self.table_conf = table_conf
        self.schema = schema

    @abstractmethod
    def add_default_transformation(self,
                                   query_config: QueryConfig) -> QueryConfig:
        pass

    @abstractmethod
    def build_sql_query(self, query_config: QueryConfig) -> str:
        try:
            sql_query = StringIO()
            transformation_dict = query_config.list_to_dict(TransformRuleMapping, "column_name")
            cols_to_be_hashed = query_config.get_comparison_columns(self.table_conf, self.schema)
            key_columns = query_config.get_key_columns(self.table_conf)

            hash_expr_list = []
            for col in cols_to_be_hashed:
                transformation_expr = TransformRuleMapping.get_column_expression_without_alias(
                    transformation_dict.get(col))
                hash_expr_list.append(transformation_expr)

            hash_expr = query_config.generate_hash_algorithm(self.source_type, hash_expr_list)

            sql_query.write("select ")
            sql_query.write(hash_expr)
            sql_query.write(f" as {Constants.hash_column_name}")

            join_expr = ",".join([col_name for col_name in key_columns])
            if join_expr:
                sql_query.write(" , ")
                sql_query.write(join_expr)

            sql_query.write(" from ")

            # table name
            if self.layer == "source":
                sql_query.write(self.table_conf.source_name)
            elif self.layer == "target":
                sql_query.write(self.table_conf.target_name)

            # where/filter clause
            if self.table_conf.filters:
                if self.layer == "source" and self.table_conf.filters.source:
                    sql_query.write(" where ")
                    sql_query.write(self.table_conf.filters.source)
                elif self.layer == "target" and self.table_conf.filters.target:
                    sql_query.write(" where ")
                    sql_query.write(self.table_conf.filters.target)

            final_sql_query = sql_query.getvalue()
            sql_query.close()
            return final_sql_query
        except Exception as e:
            message = f"An error occurred in method generate_full_query: {e!s}"
            logger.error(message)
            raise Exception(message) from e
