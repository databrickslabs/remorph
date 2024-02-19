from databricks.labs.remorph.reconcile.constants import ColumnTransformationType, Constants, SourceType
from databricks.labs.remorph.reconcile.query_builder.query_builder import QueryBuilder
from databricks.labs.remorph.reconcile.recon_config import Tables, Schema, QueryConfig, TransformRuleMapping
from databricks.labs.remorph.reconcile.utils import filter_list


class DatabricksQueryBuilder(QueryBuilder):

    def __init__(self, layer: str, table_conf: Tables, schema: list[Schema]):
        super().__init__(layer, table_conf, schema)

    def get_cols_to_be_hashed(self):
        return super().get_cols_to_be_hashed()

    def get_columns_to_be_selected(self, query_config):
        if self.table_conf.join_columns:
            if self.layer == "source":
                join_columns = [join.source_name for join in self.table_conf.join_columns]
                query_config.select_columns += join_columns
            else:
                join_columns = [join.target_name for join in self.table_conf.join_columns]
                self._column_alias(join_columns, query_config)
        return query_config

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
            transformation_mapping = TransformRuleMapping(column, None)
            transformation_mapping.transformation = ColumnTransformationType.ORACLE_DEFAULT.value.format(column)

            default_rule.append(transformation_mapping)

        query_config.hash_col_transformation += default_rule

        return query_config

    def generate_hash_column(self, query_config: QueryConfig) -> QueryConfig:
        column_expr = [rule.transformation for rule in query_config.hash_col_transformation]
        concat_columns = " || ".join(column_expr)
        hash_algo = Constants.hash_algorithm_mapping.get(SourceType.DATABRICKS.value).get(self.layer)
        query_config.hash_expr = hash_algo.format(concat_columns)
        return query_config

    def _column_alias(self, sel_cols: list[str], query_config: QueryConfig) -> QueryConfig:

        if self.table_conf.column_mapping is not None or self.table_conf.column_mapping:
            for column_name in sel_cols:
                for i in self.table_conf.column_mapping:
                    alias_name = i.get_column_alias(column_name)
                    if alias_name:
                        query_config.select_columns.append(f"{column_name} as {alias_name}")

        return query_config

    def build_sql_query(self, query_config: QueryConfig) -> str:
        return super().build_sql_query(query_config)
