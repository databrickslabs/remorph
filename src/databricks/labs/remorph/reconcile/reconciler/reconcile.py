from databricks.labs.remorph.reconcile.query_builder.query_adapter import QueryBuilderAdapterFactory
from databricks.labs.remorph.reconcile.query_builder.query_builder import QueryBuilder


def reconcile(source_type, table_conf, schema):
    src_query_builder = QueryBuilderAdapterFactory.generate_query(source_type, "source" , table_conf, schema)

    src_sql_query = get_sql_query(src_query_builder)


def get_sql_query(query_builder: QueryBuilder):
    return (query_builder
            .get_cols_to_be_hashed()
            .transform(query_builder.get_columns_to_be_selected)
            .transform(query_builder.add_custom_transformation)
            .transform(query_builder.add_default_transformation)
            .transform(query_builder.generate_hash_column)
            .transform(query_builder.build_sql_query))
