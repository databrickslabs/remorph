from databricks.labs.remorph.reconcile.constants import ColumnTransformationType, Constants
from databricks.labs.remorph.reconcile.query_builder.source_query_build_adapter import (
    SourceQueryBuildAdapter,
)
from databricks.labs.remorph.reconcile.recon_config import QueryColumnConfig, QueryColumnWithTransformation, Tables, \
    Schema


class OracleQueryBuildAdapter(SourceQueryBuildAdapter):

    def __init__(self, source_type: str, table_conf: Tables, schema: list[Schema]):
        super().__init__(source_type, table_conf, schema)

    def get_select_columns(self) -> QueryColumnConfig:
        sel_cols = [sch.column_name for sch in self.schema]
        return QueryColumnConfig(select_cols=sel_cols, join_cols=[])

    # @abstractmethod
    # def remove_drop_cols_from_sel_cols(self) -> QueryColumnConfig:
    #     pass

    def get_join_columns(self, col_config) -> QueryColumnConfig:
        setattr(col_config, 'join_cols', [self.table_conf.join_columns])
        return col_config

    def get_jdbc_partition_column(self, col_config) -> QueryColumnConfig:
        setattr(col_config, 'jdbc_partition_col', [self.table_conf.jdbc_reader_options.partition_column])
        return col_config

    def add_default_transformation_to_cols(self, col_config: QueryColumnConfig) -> QueryColumnWithTransformation:
        cols_to_be_transformed = col_config.select_cols
        transformed_cols = {}
        for column in cols_to_be_transformed:
            transformed_cols[column] = ColumnTransformationType.ORACLE_DEFAULT.value.format(column)
        return QueryColumnWithTransformation(transformed_cols)

    def generate_hash_column(self,
                             transformation_config: QueryColumnWithTransformation) -> QueryColumnWithTransformation:
        try:
            concat_string = " || ".join(transformation_config.cols_transformed.values())
            setattr(transformation_config, 'hash_col', concat_string)
            return transformation_config
        except Exception as e:
            message = f"An error occurred in method generate_hash_column: {str(e)}"
            print(message)
            raise Exception(message)

    def generate_hash_algorithm(self,
                                transformation_config: QueryColumnWithTransformation) -> QueryColumnWithTransformation:
        hash_column = (Constants.hash_algorithm_mapping.get(self.source_type).get("source")).format(
            transformation_config.hash_col)
        setattr(transformation_config, 'hash_col', hash_column)
        return transformation_config

    def generate_sql_query(self) -> str:
        print(123)
