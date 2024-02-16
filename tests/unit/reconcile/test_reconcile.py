from databricks.labs.remorph.reconcile.constants import SourceType
from databricks.labs.remorph.reconcile.query_builder.query_adapter import QueryBuilderAdapterFactory
from databricks.labs.remorph.reconcile.recon_config import Schema, Tables, JdbcReaderOptions, \
    JoinColumns
from databricks.labs.remorph.reconcile.reconciler.reconcile import get_sql_query


def test_reconcile():
    table_conf = Tables(source_name="test_emp",
                        target_name="test_emp",
                        jdbc_reader_options=JdbcReaderOptions(number_partitions=2,partition_column="id",
                                                              lower_bound="0", upper_bound="100"),
                        join_columns=[JoinColumns(source_name="id", target_name="id")],
                        select_columns=None,
                        drop_columns=None,
                        column_mapping=None,
                        transformations=None,
                        thresholds=None,
                        filters=None)
    schema = [Schema("id", "integer"), Schema("name", "string"), Schema("sal", "double")]

    src_query_builder = QueryBuilderAdapterFactory.generate_query(SourceType.ORACLE.value, "source", table_conf, schema)

    actual_query = get_sql_query(src_query_builder)

    expected_query = """select lower(RAWTOHEX(STANDARD_HASH(coalesce(trim(id),'') || coalesce(trim(name),'') || coalesce(trim(sal),''), 'SHA256'))) as hash_value__recon , id from test_emp"""

    assert actual_query == expected_query
