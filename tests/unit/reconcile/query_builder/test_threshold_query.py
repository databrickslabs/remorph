from databricks.labs.remorph.reconcile.query_builder.threshold_query import (
    ThresholdQueryBuilder,
)
from databricks.labs.remorph.reconcile.recon_config import (
    ColumnMapping,
    JdbcReaderOptions,
    Table,
    Thresholds,
    Transformation,
)
from tests.unit.reconcile.query_builder.schemas import alias_schema, schema


def test_threshold_query_builder_with_defaults():
    table_conf = Table(
        source_name="supplier",
        target_name="supplier",
        jdbc_reader_options=None,
        join_columns=["s_suppkey"],
        select_columns=None,
        drop_columns=None,
        column_mapping=None,
        transformations=None,
        thresholds=[Thresholds(column_name="s_acctbal", lower_bound="0", upper_bound="100", type="int")],
        filters=None,
    )

    actual_src_query = ThresholdQueryBuilder(table_conf, schema, "source", "oracle").build_query()
    expected_src_query = (
        'select s_acctbal as s_acctbal,s_suppkey as s_suppkey from {schema_name}.supplier where  1 = 1 '
    )
    assert actual_src_query == expected_src_query

    actual_tgt_query = ThresholdQueryBuilder(table_conf, schema, "target", "databricks").build_query()
    expected_tgt_query = (
        'select s_acctbal as s_acctbal,s_suppkey as s_suppkey from {catalog_name}.{schema_name}.supplier where  1 = 1 '
    )
    assert actual_tgt_query == expected_tgt_query


def test_threshold_query_builder_with_transformations_and_jdbc():
    table_conf = Table(
        source_name="supplier",
        target_name="supplier",
        jdbc_reader_options=JdbcReaderOptions(
            number_partitions=100, partition_column="s_nationkey", lower_bound="0", upper_bound="100"
        ),
        join_columns=["s_suppkey"],
        select_columns=None,
        drop_columns=["s_comment"],
        column_mapping=[
            ColumnMapping(source_name="s_suppkey", target_name="s_suppkey_t"),
            ColumnMapping(source_name="s_address", target_name="s_address_t"),
            ColumnMapping(source_name="s_nationkey", target_name="s_nationkey_t"),
            ColumnMapping(source_name="s_phone", target_name="s_phone_t"),
            ColumnMapping(source_name="s_acctbal", target_name="s_acctbal_t"),
            ColumnMapping(source_name="s_comment", target_name="s_comment_t"),
            ColumnMapping(source_name="s_suppdate", target_name="s_suppdate_t"),
        ],
        transformations=[
            Transformation(column_name="s_suppkey", source="trim(s_suppkey)", target="trim(s_suppkey_t)"),
            Transformation(column_name="s_address", source="trim(s_address)", target="trim(s_address_t)"),
            Transformation(column_name="s_phone", source="trim(s_phone)", target="trim(s_phone_t)"),
            Transformation(column_name="s_name", source="trim(s_name)", target="trim(s_name)"),
            Transformation(
                column_name="s_acctbal",
                source="trim(to_char(s_acctbal, '9999999999.99'))",
                target="cast(s_acctbal_t as decimal(38,2))",
            ),
        ],
        thresholds=[
            Thresholds(column_name="s_acctbal", lower_bound="0", upper_bound="100", type="int"),
            Thresholds(column_name="s_suppdate", lower_bound="-86400", upper_bound="86400", type="timestamp"),
        ],
        filters=None,
    )

    actual_src_query = ThresholdQueryBuilder(table_conf, schema, "source", "oracle").build_query()
    expected_src_query = (
        "select trim(to_char(s_acctbal, '9999999999.99')) as s_acctbal,s_nationkey "
        "as s_nationkey,s_suppdate as s_suppdate,trim(s_suppkey) as s_suppkey from "
        "{schema_name}.supplier where  1 = 1 "
    )
    assert actual_src_query == expected_src_query

    actual_tgt_query = ThresholdQueryBuilder(table_conf, alias_schema, "target", "databricks").build_query()
    expected_tgt_query = (
        "select cast(s_acctbal_t as decimal(38,2)) as s_acctbal,s_suppdate_t as "
        "s_suppdate,trim(s_suppkey_t) as s_suppkey from {catalog_name}.{schema_name}.supplier where  1 = 1 "
    )

    assert actual_tgt_query == expected_tgt_query
