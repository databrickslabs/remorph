from databricks.labs.remorph.reconcile.query_builder.adapter import QueryBuilderAdapterFactory
from databricks.labs.remorph.reconcile.query_builder.configurator import QueryConfig
from databricks.labs.remorph.reconcile.recon_config import Tables, Schema


class HashQueryGenerator:

    def __init__(self, source_type: str, table_conf: Tables, schema: list[Schema], layer: str):
        self.source_type = source_type
        self.table_conf = table_conf
        self.schema = schema
        self.layer = layer

    def generate_hash_query(self):
        cols_list = [schema.column_name for schema in self.schema]
        query_config = QueryConfig(table_transform=[])
        query_builder = QueryBuilderAdapterFactory.create(source_type=self.source_type,
                                                          table_conf=self.table_conf,
                                                          schema=self.schema)

        custom_transformation = query_config.add_custom_transformations(self.table_conf, cols_list, self.layer)
        default_transformation = query_builder.add_default_transformation(custom_transformation)
        hash_query = query_builder.build_sql_query(default_transformation)

        return hash_query
