from databricks.labs.remorph.reconcile.constants import ColumnTransformationType
from databricks.labs.remorph.reconcile.query_builder.builder import QueryBuilder
from databricks.labs.remorph.reconcile.query_builder.configurator import QueryConfig
from databricks.labs.remorph.reconcile.recon_config import Tables, Schema, TransformRuleMapping


class OracleQueryBuilder(QueryBuilder):

    def __init__(self, source_type: str, layer: str, table_conf: Tables, schema: list[Schema]):
        super().__init__(source_type, layer, table_conf, schema)

    def add_default_transformation(self,
                                   query_config: QueryConfig) -> QueryConfig:
        cols_to_apply_default_transformation = [transformRule.column_name for transformRule in
                                                query_config.table_transform if transformRule.transformation is None]

        transform_list = query_config.list_to_dict(TransformRuleMapping, "column_name")

        for column in cols_to_apply_default_transformation:
            transformation_rule = transform_list.get(column)
            transformation_rule.transformation = ColumnTransformationType.ORACLE_DEFAULT.value.format(column)

        return query_config

    def build_sql_query(self, query_config: QueryConfig) -> str:
        return super().build_sql_query(query_config)
