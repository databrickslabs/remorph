from databricks.labs.remorph.reconcile.query_builder.query_adapter import QueryBuilderAdapterFactory
from databricks.labs.remorph.reconcile.query_builder.query_configurator import QueryConfig
from databricks.labs.remorph.reconcile.recon_config import Tables, Schema, TransformRuleMapping


def reconcile(source_type: str, table_conf: Tables, schema: list[Schema]):
    cols_list = [schema.column_name for schema in schema]
    source_query_config = QueryConfig(table_transform=[])
    source_query_builder = QueryBuilderAdapterFactory.generate_query(source_type=source_type, table_conf=table_conf,
                                                                     schema=schema)

    custom_transformation = source_query_config.add_custom_transformations(table_conf, cols_list, "source")
    default_transformation = source_query_builder.add_default_transformation(custom_transformation)
    src_hash_query = source_query_builder.build_sql_query(default_transformation)

    return src_hash_query
