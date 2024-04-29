from databricks.labs.remorph.reconcile.query_builder.hash_query import HashQueryBuilder


def test_hash_query_builder(table_conf_with_opts, schema):
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
