from databricks.labs.remorph.reconcile.query_builder.hash_query import HashQueryBuilder
from databricks.labs.remorph.reconcile.recon_config import ColumnMapping, Filters


def test_hash_query_builder_for_snowflake_src(table_conf_with_opts, schema):
    sch, sch_with_alias = schema
    src_actual = HashQueryBuilder(table_conf_with_opts, sch, "source", "snowflake").build_query()
    src_expected = (
        "SELECT LOWER(SHA2(CONCAT(TRIM(s_address), TRIM(s_name), COALESCE(TRIM(s_nationkey), ''), "
        "TRIM(s_phone), COALESCE(TRIM(s_suppkey), '')), 256)) AS hash_value_recon, COALESCE(TRIM("
        "s_nationkey), '') AS s_nationkey, COALESCE(TRIM(s_suppkey), '') AS s_suppkey FROM :tbl WHERE "
        "s_name = 't' AND s_address = 'a'"
    )

    tgt_actual = HashQueryBuilder(table_conf_with_opts, sch_with_alias, "target", "databricks").build_query()
    tgt_expected = (
        "SELECT LOWER(SHA2(CONCAT(TRIM(s_address_t), TRIM(s_name), COALESCE(TRIM(s_nationkey_t), ''), "
        "TRIM(s_phone_t), COALESCE(TRIM(s_suppkey_t), '')), 256)) AS hash_value_recon, COALESCE(TRIM("
        "s_nationkey_t), '') AS s_nationkey, COALESCE(TRIM(s_suppkey_t), '') AS s_suppkey FROM :tbl WHERE "
        "s_name = 't' AND s_address_t = 'a'"
    )

    assert src_actual == src_expected
    assert tgt_actual == tgt_expected


def test_hash_query_builder_for_oracle_src(table_conf_mock, schema):
    table_conf = table_conf_mock(
        join_columns=["s_suppkey", "s_nationkey"],
        column_mapping=[
            ColumnMapping(source_name="s_suppkey", target_name="s_suppkey_t"),
            ColumnMapping(source_name="s_nationkey", target_name='s_nationkey_t'),
            ColumnMapping(source_name="s_address", target_name="s_address_t"),
            ColumnMapping(source_name="s_phone", target_name="s_phone_t"),
            ColumnMapping(source_name="s_acctbal", target_name="s_acctbal_t"),
            ColumnMapping(source_name="s_comment", target_name="s_comment_t"),
        ],
        filters=Filters(source="s_nationkey=1"),
    )
    sch, sch_with_alias = schema
    src_actual = HashQueryBuilder(table_conf, sch, "source", "oracle").build_query()
    src_expected = (
        "SELECT LOWER(RAWTOHEX(STANDARD_HASH(CONCAT(COALESCE(TRIM(s_acctbal), ''), COALESCE(TRIM(s_address), ''), "
        "COALESCE(TRIM(s_comment), ''), COALESCE(TRIM(s_name), ''), COALESCE(TRIM(s_nationkey), ''), COALESCE(TRIM("
        "s_phone), ''), COALESCE(TRIM(s_suppkey), '')), 'SHA256'))) AS hash_value_recon, COALESCE(TRIM(s_nationkey), "
        "'') AS s_nationkey, COALESCE(TRIM(s_suppkey), '') AS s_suppkey FROM :tbl WHERE s_nationkey = 1"
    )

    tgt_actual = HashQueryBuilder(table_conf, sch_with_alias, "target", "databricks").build_query()
    tgt_expected = (
        "SELECT LOWER(SHA2(CONCAT(COALESCE(TRIM(s_acctbal_t), ''), COALESCE(TRIM(s_address_t), ''), COALESCE(TRIM("
        "s_comment_t), ''), COALESCE(TRIM(s_name), ''), COALESCE(TRIM(s_nationkey_t), ''), COALESCE(TRIM(s_phone_t), "
        "''), COALESCE(TRIM(s_suppkey_t), '')), 256)) AS hash_value_recon, COALESCE(TRIM(s_nationkey_t), "
        "'') AS s_nationkey, COALESCE(TRIM(s_suppkey_t), '') AS s_suppkey FROM :tbl"
    )

    assert src_actual == src_expected
    assert tgt_actual == tgt_expected
