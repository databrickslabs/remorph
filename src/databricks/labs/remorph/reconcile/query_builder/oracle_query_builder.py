from databricks.labs.remorph.reconcile.constants import ColumnTransformationType, Constants, SourceType
from databricks.labs.remorph.reconcile.query_builder.query_builder import QueryBuilder
from databricks.labs.remorph.reconcile.recon_config import Tables, Schema, QueryConfig, TransformRuleMapping
from databricks.labs.remorph.reconcile.utils import filter_list


class OracleQueryBuilder(QueryBuilder):

    def __init__(self, layer: str, table_conf: Tables, schema: list[Schema]):
        super().__init__(layer, table_conf, schema)

    def get_cols_to_be_hashed(self):
        return super().get_cols_to_be_hashed()

    def get_columns_to_be_selected(self, query_config):
        return super().get_columns_to_be_selected(query_config)

    def add_custom_transformation(self, query_config: QueryConfig):
        return super().add_custom_transformation(query_config)

    def add_default_transformation(self,
                                   query_config: QueryConfig) -> QueryConfig:
        default_rule: list[TransformRuleMapping] = []

        cols_with_custom_transformation = [transformRule.column_name for transformRule in
                                           query_config.hash_col_transformation]
        cols_to_apply_default_transformation = filter_list(input_list=query_config.hash_columns,
                                                           remove_list=cols_with_custom_transformation)

        for column in cols_to_apply_default_transformation:
            transformation_mapping = TransformRuleMapping(column, None, None)
            transformation_mapping.transformation = ColumnTransformationType.ORACLE_DEFAULT.value.format(column)

            default_rule.append(transformation_mapping)

        query_config.hash_col_transformation += default_rule

        return query_config

    def generate_hash_column(self, query_config: QueryConfig) -> QueryConfig:
        column_expr = [rule.transformation for rule in query_config.hash_col_transformation]
        concat_columns = " || ".join(column_expr)
        hash_algo = Constants.hash_algorithm_mapping.get(SourceType.ORACLE.value).get(self.layer)
        query_config.hash_expr = hash_algo.format(concat_columns)
        return query_config

    def build_sql_query(self, query_config: QueryConfig) -> str:
        return super().build_sql_query(query_config)
