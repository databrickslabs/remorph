from dataclasses import asdict

from databricks.labs.remorph.reconcile.recon_config import QueryColumnConfig, Schema, Tables, JdbcReaderOptions, \
    JoinColumns, QueryColumnWithTransformation
from databricks.labs.remorph.reconcile.reconciler.reconcile import reconcile


def test_reconcile():
    table_conf = Tables(source_name="emp",
                        target_name="emp",
                        jdbc_reader_options=JdbcReaderOptions(number_partitions=2, partition_column="id",
                                                              lower_bound="0", upper_bound="100"),
                        join_columns=[JoinColumns(source_name="id", target_name="id")],
                        column_mapping=None,
                        transformations=None,
                        thresholds=None,
                        filters=None)
    schema = [Schema("id", "integer"), Schema("name", "string"), Schema("sal", "double")]
    query_build = reconcile("oracle", table_conf, schema)

    col_config = query_build[0]
    transformation_config = query_build[1]

    expected_col_config = QueryColumnConfig(select_cols=['id', 'name', 'sal'],
                                            join_cols=[[JoinColumns(source_name='id', target_name='id')]],
                                            jdbc_partition_col=['id'])

    expected_transformation_config = QueryColumnWithTransformation(
        cols_transformed={'id': "coalesce(trim(id),'')", 'name': "coalesce(trim(name),'')",
                          'sal': "coalesce(trim(sal),'')"},
        hash_col="lower(RAWTOHEX(STANDARD_HASH(coalesce(trim(id),'') || coalesce(trim(name),'') || coalesce(trim("
                 "sal),''), 'SHA256')))")

    assert asdict(col_config) == asdict(expected_col_config)
    assert asdict(transformation_config) == asdict(expected_transformation_config)
