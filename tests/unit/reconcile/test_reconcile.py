from databricks.labs.remorph.reconcile.constants import SourceType
from databricks.labs.remorph.reconcile.query_builder.query_adapter import QueryBuilderAdapterFactory
from databricks.labs.remorph.reconcile.recon_config import Schema, Tables, JdbcReaderOptions, \
    JoinColumns, ColumnMapping
from databricks.labs.remorph.reconcile.reconciler.reconcile import get_sql_query


def test_query_builder_source_oracle():
    table_conf = Tables(source_name="test_emp",
                        target_name="test_emp",
                        jdbc_reader_options=JdbcReaderOptions(number_partitions=2, partition_column="id",
                                                              lower_bound="0", upper_bound="100"),
                        join_columns=[JoinColumns(source_name="id", target_name="id")],
                        select_columns=None,
                        drop_columns=None,
                        column_mapping=None,
                        transformations=None,
                        thresholds=None,
                        filters=None)
    schema = [Schema("id", "integer"), Schema("name", "string"), Schema("sal", "double")]

    src_query_builder = QueryBuilderAdapterFactory.generate_src_query(SourceType.ORACLE.value, table_conf,
                                                                      schema)

    actual_query = get_sql_query(src_query_builder)

    expected_query = """select lower(RAWTOHEX(STANDARD_HASH(coalesce(trim(id),'') || coalesce(trim(name),'') || coalesce(trim(sal),''), 'SHA256'))) as hash_value__recon , id from test_emp"""

    assert actual_query == expected_query


def test_query_builder_source_databricks():
    table_conf = Tables(source_name="test_emp",
                        target_name="test_emp",
                        jdbc_reader_options=JdbcReaderOptions(number_partitions=2, partition_column="id",
                                                              lower_bound="0", upper_bound="100"),
                        join_columns=[JoinColumns(source_name="id", target_name="id_no")],
                        select_columns=None,
                        drop_columns=None,
                        column_mapping=[ColumnMapping("id_no", "id")],
                        transformations=None,
                        thresholds=None,
                        filters=None)
    schema = [Schema("id", "integer"), Schema("name", "string"), Schema("sal", "double")]

    src_query_builder = QueryBuilderAdapterFactory.generate_src_query(SourceType.DATABRICKS.value, table_conf,
                                                                      schema)

    actual_query = get_sql_query(src_query_builder)

    expected_query = """select sha2(coalesce(trim(id),'') || coalesce(trim(name),'') || coalesce(trim(sal),''),256) as hash_value__recon , id from test_emp"""

    assert actual_query == expected_query


def test_query_builder_target():
    table_conf = Tables(source_name="test_emp",
                        target_name="test_emp",
                        jdbc_reader_options=JdbcReaderOptions(number_partitions=2, partition_column="id",
                                                              lower_bound="0", upper_bound="100"),
                        join_columns=[JoinColumns(source_name="id", target_name="id_no")],
                        select_columns=None,
                        drop_columns=None,
                        column_mapping=[ColumnMapping("id_no", "id")],
                        transformations=None,
                        thresholds=None,
                        filters=None)
    schema = [Schema("id_no", "integer"), Schema("name", "string"), Schema("sal", "double")]

    src_query_builder = QueryBuilderAdapterFactory.generate_tgt_query(table_conf, schema)

    actual_query = get_sql_query(src_query_builder)

    expected_query = """select sha2(coalesce(trim(id_no),'') || coalesce(trim(name),'') || coalesce(trim(sal),''),256) as hash_value__recon , id_no as id from test_emp"""

    assert actual_query == expected_query
