from databricks.labs.remorph.reconcile.query_builder.source_query_builder import SourceQueryBuilderFactory


def reconcile(source_type, table_conf, schema):
    source_query_builder = SourceQueryBuilderFactory.create(source_type=source_type, table_conf=table_conf,
                                                            schema=schema)

    column_config = (source_query_builder
                     .get_select_columns()
                     .transform(source_query_builder.get_join_columns)
                     .transform(source_query_builder.get_jdbc_partition_column)
                     )

    column_transformation_config = (source_query_builder.add_default_transformation_to_cols(column_config)
                                    .transform(source_query_builder.generate_hash_column)
                                    .transform(source_query_builder.generate_hash_algorithm)
                                    )

    return column_config, column_transformation_config
