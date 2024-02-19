from abc import ABC, abstractmethod
from io import StringIO

from databricks.labs.blueprint.entrypoint import get_logger
from databricks.labs.remorph.reconcile.constants import Constants
from databricks.labs.remorph.reconcile.recon_config import Tables, Schema, QueryConfig, TransformRuleMapping, \
    Transformation
from databricks.labs.remorph.reconcile.utils import filter_list

logger = get_logger(__file__)


class QueryBuilder(ABC):

    def __init__(self, layer: str, table_conf: Tables, schema: list[Schema]):
        self.layer = layer
        self.table_conf = table_conf
        self.schema = schema

    @abstractmethod
    def get_cols_to_be_hashed(self) -> QueryConfig:

        cols_to_be_hashed = []
        # get threshold columns
        if self.table_conf.thresholds:
            threshold_cols = [threshold.column_name for threshold in self.table_conf.thresholds]
        else:
            threshold_cols = []
        # explicit select columns
        if self.table_conf.select_columns:
            sel_cols = filter_list(input_list=self.table_conf.select_columns, remove_list=threshold_cols)
            join_cols = [join.source_name for join in self.table_conf.join_columns]
            cols_to_be_hashed += (sel_cols + join_cols)
        # complete schema is considered here
        else:
            sel_cols = [schema.column_name for schema in self.schema]
            drop_cols = self.table_conf.drop_columns
            if drop_cols is None:
                drop_cols = []
            final_sel_cols = filter_list(input_list=sel_cols, remove_list=drop_cols + threshold_cols)
            cols_to_be_hashed += final_sel_cols

        return QueryConfig(hash_columns=cols_to_be_hashed, select_columns=[], hash_col_transformation=[],
                           hash_expr=None)

    @abstractmethod
    def get_columns_to_be_selected(self, query_config: QueryConfig) -> QueryConfig:

        if self.table_conf.join_columns:
            join_columns = [join.source_name for join in self.table_conf.join_columns]
            partition_column = self.table_conf.jdbc_reader_options.partition_column
            if partition_column not in join_columns:
                join_columns.append(partition_column)
            query_config.select_columns += join_columns

        return query_config

    @abstractmethod
    def add_custom_transformation(
            self, query_config: QueryConfig
    ) -> QueryConfig:
        transformation_dict = self.table_conf.list_to_dict(Transformation, "column_name")

        if transformation_dict is not None:
            for column in query_config.hash_columns:
                transformation_mapping = TransformRuleMapping(column, None)
                if column in transformation_dict.keys():
                    match self.layer:
                        case "source":
                            transformation_mapping.transformation = transformation_dict.get(column).source
                        case "target":
                            transformation_mapping.transformation = transformation_dict.get(column).target
                        case _:
                            print("Invalid layer value only source or target is allowed")
                    query_config.hash_col_transformation.append(transformation_mapping)

        return query_config

    @abstractmethod
    def add_default_transformation(self,
                                   query_config: QueryConfig) -> QueryConfig:
        pass

    @abstractmethod
    def generate_hash_column(self, query_config: QueryConfig) -> str:
        pass

    @abstractmethod
    def build_sql_query(self, query_config: QueryConfig) -> str:
        try:
            sql_query = StringIO()

            sql_query.write("select ")
            sql_query.write(query_config.hash_expr)
            sql_query.write(f" as {Constants.hash_column_name}")

            join_expr = ",".join([col_name for col_name in query_config.select_columns])
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
