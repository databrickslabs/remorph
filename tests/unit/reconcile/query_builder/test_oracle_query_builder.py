import pytest

from databricks.labs.remorph.reconcile.constants import SourceType
from databricks.labs.remorph.reconcile.query_builder.query_adapter import QueryBuilderAdapterFactory
from databricks.labs.remorph.reconcile.recon_config import Tables, JdbcReaderOptions, JoinColumns, Schema, QueryConfig, \
    TransformRuleMapping
from tests.unit.reconcile.query_builder.conftest import assert_query_config_dataclass


@pytest.fixture
def oracle_query_builder():
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

    query_builder = QueryBuilderAdapterFactory.generate_src_query(SourceType.ORACLE.value, table_conf, schema)

    return query_builder


def test_add_default_transformation(oracle_query_builder):
    test_query_config = QueryConfig(
        [TransformRuleMapping(column_name='id', transformation="coalesce(trim(id),'')", alias_name=None),
         TransformRuleMapping(column_name='name', transformation=None, alias_name=None),
         TransformRuleMapping(column_name='sal', transformation="coalesce(trim(sal),'')", alias_name=None)])

    actual = oracle_query_builder.add_default_transformation(test_query_config)
    expected = QueryConfig(table_transform=
                           [TransformRuleMapping(column_name='id', transformation="coalesce(trim(id),'')",
                                                 alias_name=None),
                            TransformRuleMapping(column_name='name', transformation="coalesce(trim(name),'')",
                                                 alias_name=None),
                            TransformRuleMapping(column_name='sal', transformation="coalesce(trim(sal),'')",
                                                 alias_name=None)])

    assert_query_config_dataclass(actual, expected)


def test_build_sql_query(oracle_query_builder):
    test_query_config = QueryConfig(table_transform=
                                    [TransformRuleMapping(column_name='id', transformation="coalesce(trim(id),'')",
                                                          alias_name=None),
                                     TransformRuleMapping(column_name='name', transformation="coalesce(trim(name),'')",
                                                          alias_name=None),
                                     TransformRuleMapping(column_name='sal', transformation="coalesce(trim(sal),'')",
                                                          alias_name=None)])

    actual = oracle_query_builder.build_sql_query(test_query_config)
    expected = "select lower(RAWTOHEX(STANDARD_HASH(coalesce(trim(id),'') || coalesce(trim(name),'') || coalesce(trim(sal),''), 'SHA256'))) as hash_value__recon , id from test_emp"

    assert actual == expected
