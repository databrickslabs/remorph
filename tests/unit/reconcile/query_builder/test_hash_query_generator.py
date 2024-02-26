import pytest

from databricks.labs.remorph.reconcile.constants import SourceType
from databricks.labs.remorph.reconcile.query_builder.generator import HashQueryGenerator
from databricks.labs.remorph.reconcile.recon_config import Tables, JdbcReaderOptions, JoinColumns, ColumnMapping, \
    Transformation, Schema


@pytest.fixture
def app_config():
    table_conf = Tables(source_name='supplier', target_name='supplier',
                        jdbc_reader_options=JdbcReaderOptions(number_partitions=10, partition_column='s_suppkey',
                                                              lower_bound="0", upper_bound="10000000", fetch_size=100),
                        join_columns=[JoinColumns(source_name='s_suppkey', target_name=None)], select_columns=None,
                        drop_columns=None,
                        column_mapping=[ColumnMapping(source_name='s_address', target_name='s_address')],
                        transformations=[
                            Transformation(column_name='s_address', source='trim(s_address)', target='trim(s_address)'),
                            Transformation(column_name='s_comment', source='trim(s_comment)', target='trim(s_comment)'),
                            Transformation(column_name='s_name', source='trim(s_name)', target='trim(s_name)'),
                            Transformation(column_name='s_acctbal', source="trim(to_char(s_acctbal, '9999999999.99'))",
                                           target='cast(s_acctbal as decimal(38,2))')], thresholds=[], filters=None)
    schema = [Schema("s_suppkey", "number"), Schema("s_name", "varchar"), Schema("s_address", "varchar"),
              Schema("s_nationkey", "number"), Schema("s_phone", "varchar"), Schema("s_acctbal", "number"),
              Schema("s_comment", "varchar")]
    return table_conf, schema


def test_hash_query_generator(app_config):
    actual_query = HashQueryGenerator(source_type=SourceType.ORACLE.value, table_conf=app_config[0],
                                      schema=app_config[1], layer="source").generate_hash_query()
    expected_query = "select lower(RAWTOHEX(STANDARD_HASH(coalesce(trim(s_suppkey),'') || trim(s_name) || trim(s_address) || coalesce(trim(s_nationkey),'') || coalesce(trim(s_phone),'') || trim(to_char(s_acctbal, '9999999999.99')) || trim(s_comment), 'SHA256'))) as hash_value__recon , s_suppkey from supplier"

    assert actual_query == expected_query
