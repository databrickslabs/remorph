from databricks.labs.remorph.config import get_dialect
from databricks.labs.remorph.reconcile.query_builder.hash_query import HashQueryBuilder
from databricks.labs.remorph.reconcile.recon_config import Filters, ColumnMapping


def test_hash_query_builder_for_snowflake_src(table_conf_with_opts, table_schema):
    sch, sch_with_alias = table_schema
    src_actual = HashQueryBuilder(table_conf_with_opts, sch, "source", get_dialect("snowflake")).build_query(
        report_type="data"
    )
    src_expected = (
        "SELECT LOWER(SHA2(CONCAT(TRIM(s_address), TRIM(s_name), COALESCE(TRIM(s_nationkey), ''), "
        "TRIM(s_phone), COALESCE(TRIM(s_suppkey), '')), 256)) AS hash_value_recon, s_nationkey AS s_nationkey, "
        "s_suppkey AS s_suppkey FROM :tbl WHERE s_name = 't' AND s_address = 'a'"
    )

    tgt_actual = HashQueryBuilder(
        table_conf_with_opts, sch_with_alias, "target", get_dialect("databricks")
    ).build_query(report_type="data")
    tgt_expected = (
        "SELECT LOWER(SHA2(CONCAT(TRIM(s_address_t), TRIM(s_name), COALESCE(TRIM(s_nationkey_t), ''), "
        "TRIM(s_phone_t), COALESCE(TRIM(s_suppkey_t), '')), 256)) AS hash_value_recon, s_nationkey_t AS s_nationkey, "
        "s_suppkey_t AS s_suppkey FROM :tbl WHERE s_name = 't' AND s_address_t = 'a'"
    )

    assert src_actual == src_expected
    assert tgt_actual == tgt_expected


def test_hash_query_builder_for_oracle_src(table_conf_mock, table_schema, column_mapping):
    schema, _ = table_schema
    table_conf = table_conf_mock(
        join_columns=["s_suppkey", "s_nationkey"],
        filters=Filters(source="s_nationkey=1"),
        column_mapping=[ColumnMapping(source_name="s_nationkey", target_name="s_nationkey")],
    )
    src_actual = HashQueryBuilder(table_conf, schema, "source", get_dialect("oracle")).build_query(report_type="all")
    src_expected = (
        "SELECT LOWER(RAWTOHEX(STANDARD_HASH(CONCAT(COALESCE(TRIM(s_acctbal), ''), COALESCE(TRIM(s_address), ''), "
        "COALESCE(TRIM(s_comment), ''), COALESCE(TRIM(s_name), ''), COALESCE(TRIM(s_nationkey), ''), COALESCE(TRIM("
        "s_phone), ''), COALESCE(TRIM(s_suppkey), '')), 'SHA256'))) AS hash_value_recon, s_nationkey AS s_nationkey, "
        "s_suppkey AS s_suppkey FROM :tbl WHERE s_nationkey = 1"
    )

    tgt_actual = HashQueryBuilder(table_conf, schema, "target", get_dialect("databricks")).build_query(
        report_type="all"
    )
    tgt_expected = (
        "SELECT LOWER(SHA2(CONCAT(COALESCE(TRIM(s_acctbal), ''), COALESCE(TRIM(s_address), ''), COALESCE(TRIM("
        "s_comment), ''), COALESCE(TRIM(s_name), ''), COALESCE(TRIM(s_nationkey), ''), COALESCE(TRIM(s_phone), "
        "''), COALESCE(TRIM(s_suppkey), '')), 256)) AS hash_value_recon, s_nationkey AS s_nationkey, s_suppkey "
        "AS s_suppkey FROM :tbl"
    )

    assert src_actual == src_expected
    assert tgt_actual == tgt_expected


def test_hash_query_builder_for_databricks_src(table_conf_mock, table_schema, column_mapping):
    table_conf = table_conf_mock(
        join_columns=["s_suppkey"],
        column_mapping=column_mapping,
        filters=Filters(target="s_nationkey_t=1"),
    )
    sch, sch_with_alias = table_schema
    src_actual = HashQueryBuilder(table_conf, sch, "source", get_dialect("databricks")).build_query(report_type="data")
    src_expected = (
        "SELECT LOWER(SHA2(CONCAT(COALESCE(TRIM(s_acctbal), ''), COALESCE(TRIM(s_address), ''), "
        "COALESCE(TRIM(s_comment), ''), COALESCE(TRIM(s_name), ''), COALESCE(TRIM(s_nationkey), ''), COALESCE(TRIM("
        "s_phone), ''), COALESCE(TRIM(s_suppkey), '')), 256)) AS hash_value_recon, s_suppkey AS s_suppkey FROM :tbl"
    )

    tgt_actual = HashQueryBuilder(table_conf, sch_with_alias, "target", get_dialect("databricks")).build_query(
        report_type="data"
    )
    tgt_expected = (
        "SELECT LOWER(SHA2(CONCAT(COALESCE(TRIM(s_acctbal_t), ''), COALESCE(TRIM(s_address_t), ''), COALESCE(TRIM("
        "s_comment_t), ''), COALESCE(TRIM(s_name), ''), COALESCE(TRIM(s_nationkey_t), ''), COALESCE(TRIM(s_phone_t), "
        "''), COALESCE(TRIM(s_suppkey_t), '')), 256)) AS hash_value_recon, s_suppkey_t AS s_suppkey FROM :tbl WHERE "
        "s_nationkey_t = 1"
    )

    assert src_actual == src_expected
    assert tgt_actual == tgt_expected


def test_hash_query_builder_for_report_type_is_row(table_conf_with_opts, table_schema, column_mapping):
    sch, sch_with_alias = table_schema
    src_actual = HashQueryBuilder(table_conf_with_opts, sch, "source", get_dialect("databricks")).build_query(
        report_type="row"
    )
    src_expected = (
        "SELECT LOWER(SHA2(CONCAT(TRIM(s_address), TRIM(s_name), COALESCE(TRIM(s_nationkey), ''), "
        "TRIM(s_phone), COALESCE(TRIM(s_suppkey), '')), 256)) AS hash_value_recon, TRIM(s_address) AS "
        "s_address, TRIM(s_name) AS s_name, s_nationkey AS s_nationkey, TRIM(s_phone) "
        "AS s_phone, s_suppkey AS s_suppkey FROM :tbl WHERE s_name = 't' AND "
        "s_address = 'a'"
    )

    tgt_actual = HashQueryBuilder(
        table_conf_with_opts, sch_with_alias, "target", get_dialect("databricks")
    ).build_query(report_type="row")
    tgt_expected = (
        "SELECT LOWER(SHA2(CONCAT(TRIM(s_address_t), TRIM(s_name), COALESCE(TRIM(s_nationkey_t), ''), "
        "TRIM(s_phone_t), COALESCE(TRIM(s_suppkey_t), '')), 256)) AS hash_value_recon, TRIM(s_address_t) "
        "AS s_address, TRIM(s_name) AS s_name, s_nationkey_t AS s_nationkey, "
        "TRIM(s_phone_t) AS s_phone, s_suppkey_t AS s_suppkey FROM :tbl WHERE s_name "
        "= 't' AND s_address_t = 'a'"
    )

    assert src_actual == src_expected
    assert tgt_actual == tgt_expected
