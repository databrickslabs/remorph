from databricks.labs.remorph.reconcile.query_builder.threshold_query import (
    ThresholdQueryBuilder,
)
from databricks.labs.remorph.reconcile.recon_config import (
    ColumnMapping,
    Schema,
    Thresholds,
    Transformation,
)
from tests.unit.reconcile.query_builder.test_conf import TestConf


def test_threshold_query_builder_with_defaults():
    table_conf = TestConf().get_table_conf_default
    schema = TestConf().get_schema
    table_conf.join_columns = ["s_suppkey"]
    table_conf.thresholds = [Thresholds(column_name="s_acctbal", lower_bound="0", upper_bound="100", type="int")]

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
    # table conf
    table_conf = TestConf().get_table_conf_all_options
    table_conf.column_mapping = [
        ColumnMapping(source_name="s_suppkey", target_name="s_suppkey_t"),
        ColumnMapping(source_name="s_address", target_name="s_address_t"),
        ColumnMapping(source_name="s_nationkey", target_name="s_nationkey_t"),
        ColumnMapping(source_name="s_phone", target_name="s_phone_t"),
        ColumnMapping(source_name="s_acctbal", target_name="s_acctbal_t"),
        ColumnMapping(source_name="s_comment", target_name="s_comment_t"),
        ColumnMapping(source_name="s_suppdate", target_name="s_suppdate_t"),
    ]
    table_conf.transformations = [
        Transformation(column_name="s_suppkey", source="trim(s_suppkey)", target="trim(s_suppkey_t)"),
        Transformation(column_name="s_address", source="trim(s_address)", target="trim(s_address_t)"),
        Transformation(column_name="s_phone", source="trim(s_phone)", target="trim(s_phone_t)"),
        Transformation(column_name="s_name", source="trim(s_name)", target="trim(s_name)"),
        Transformation(
            column_name="s_acctbal",
            source="trim(to_char(s_acctbal, '9999999999.99'))",
            target="cast(s_acctbal_t as decimal(38,2))",
        ),
    ]
    table_conf.thresholds = [
        Thresholds(column_name="s_acctbal", lower_bound="0", upper_bound="100", type="int"),
        Thresholds(column_name="s_suppdate", lower_bound="-86400", upper_bound="86400", type="timestamp"),
    ]

    # schema
    schema = TestConf().get_schema
    schema.append(Schema("s_suppdate", "timestamp"))
    alias_schema = TestConf().get_alias_schema
    alias_schema.append(Schema("s_suppdate_t", "timestamp"))

    actual_src_query = ThresholdQueryBuilder(table_conf, schema, "source", "oracle").build_query()
    expected_src_query = (
        "select trim(to_char(s_acctbal, '9999999999.99')) as s_acctbal,s_nationkey "
        "as s_nationkey,s_suppdate as s_suppdate,trim(s_suppkey) as s_suppkey from "
        "{schema_name}.supplier where s_name='t' and s_address='a'"
    )
    assert actual_src_query == expected_src_query

    actual_tgt_query = ThresholdQueryBuilder(table_conf, alias_schema, "target", "databricks").build_query()
    expected_tgt_query = (
        "select cast(s_acctbal_t as decimal(38,2)) as s_acctbal,s_suppdate_t as "
        "s_suppdate,trim(s_suppkey_t) as s_suppkey from {catalog_name}.{schema_name}.target_supplier where s_name='t' "
        "and s_address_t='a'"
    )

    assert actual_tgt_query == expected_tgt_query
