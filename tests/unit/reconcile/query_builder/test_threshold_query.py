from databricks.labs.remorph.reconcile.query_builder.threshold_query import (
    ThresholdQueryBuilder,
)
from databricks.labs.remorph.reconcile.recon_config import (
    ColumnMapping,
    Filters,
    JdbcReaderOptions,
    Schema,
    Thresholds,
    Transformation,
)


def test_threshold_query_builder_with_defaults(table_conf_mock, schema):
    table_conf = table_conf_mock(
        join_columns=["s_suppkey"],
        thresholds=[Thresholds(column_name="s_acctbal", lower_bound="0", upper_bound="100", type="int")],
    )
    sch, _ = schema

    actual_src_query = ThresholdQueryBuilder(table_conf, sch, "source", "oracle").build_query()
    expected_src_query = 'select s_acctbal as s_acctbal,s_suppkey as s_suppkey from {schema_name}.supplier '
    assert actual_src_query == expected_src_query

    actual_tgt_query = ThresholdQueryBuilder(table_conf, sch, "target", "databricks").build_query()
    expected_tgt_query = (
        'select s_acctbal as s_acctbal,s_suppkey as s_suppkey from {catalog_name}.{schema_name}.supplier '
    )
    assert actual_tgt_query == expected_tgt_query


def test_threshold_query_builder_with_transformations_and_jdbc(table_conf_mock, schema):
    # table conf
    table_conf = table_conf_mock(
        join_columns=["s_suppkey"],
        jdbc_reader_options=JdbcReaderOptions(
            number_partitions=100, partition_column="s_nationkey", lower_bound="0", upper_bound="100"
        ),
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
        filters=Filters(source="s_name='t' and s_address='a'", target="s_name='t' and s_address_t='a'"),
    )

    # schema
    sch, sch_with_alias = schema
    sch.append(Schema("s_suppdate", "timestamp"))
    sch_with_alias.append(Schema("s_suppdate_t", "timestamp"))

    actual_src_query = ThresholdQueryBuilder(table_conf, sch, "source", "oracle").build_query()
    expected_src_query = (
        "select trim(to_char(s_acctbal, '9999999999.99')) as s_acctbal,s_nationkey "
        "as s_nationkey,s_suppdate as s_suppdate,trim(s_suppkey) as s_suppkey from "
        "{schema_name}.supplier where s_name='t' and s_address='a'"
    )
    assert actual_src_query == expected_src_query

    actual_tgt_query = ThresholdQueryBuilder(table_conf, sch_with_alias, "target", "databricks").build_query()
    expected_tgt_query = (
        "select cast(s_acctbal_t as decimal(38,2)) as s_acctbal,s_suppdate_t as "
        "s_suppdate,trim(s_suppkey_t) as s_suppkey from {catalog_name}.{schema_name}.supplier where s_name='t' "
        "and s_address_t='a'"
    )

    assert actual_tgt_query == expected_tgt_query
