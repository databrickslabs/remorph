import pytest

from databricks.labs.remorph.reconcile.query_builder.hash_query import HashQueryBuilder
from databricks.labs.remorph.reconcile.recon_config import Schema
from tests.unit.reconcile.query_builder.test_conf import TestConf


def test_hash_query_builder_without_defaults():
    table_conf = TestConf().get_table_conf_default
    schema = TestConf().get_schema
    actual_src_query = HashQueryBuilder(table_conf, schema, "source", "oracle").build_query()
    expected_src_query = (
        "select lower(RAWTOHEX(STANDARD_HASH(coalesce(trim(s_acctbal),'') || "
        "coalesce(trim(s_address),'') || coalesce(trim(s_comment),'') || "
        "coalesce(trim(s_name),'') || coalesce(trim(s_nationkey),'') || "
        "coalesce(trim(s_phone),'') || coalesce(trim(s_suppkey),''), 'SHA256'))) as "
        "hash_value__recon from {schema_name}.supplier "
        "where  1 = 1 "
    )
    assert actual_src_query == expected_src_query

    actual_tgt_query = HashQueryBuilder(table_conf, schema, "target", "databricks").build_query()
    expected_tgt_query = (
        "select sha2(concat(coalesce(trim(s_acctbal),''), "
        "coalesce(trim(s_address),''), coalesce(trim(s_comment),''), "
        "coalesce(trim(s_name),''), coalesce(trim(s_nationkey),''), "
        "coalesce(trim(s_phone),''), coalesce(trim(s_suppkey),'')),256) as "
        "hash_value__recon from {catalog_name}.{schema_name}.supplier "
        "where  1 = 1 "
    )
    assert actual_tgt_query == expected_tgt_query


def test_hash_query_builder_with_all_options():
    table_conf = TestConf().get_table_conf_all_options
    schema = TestConf().get_schema
    actual_src_query = HashQueryBuilder(table_conf, schema, "source", "oracle").build_query()
    expected_src_query = (
        "select lower(RAWTOHEX(STANDARD_HASH(coalesce(trim(s_suppkey),'') || "
        "trim(s_address) || trim(s_name), 'SHA256'))) as "
        "hash_value__recon, coalesce(trim(s_nationkey),'') as "
        "s_nationkey,coalesce(trim(s_suppkey),'') as s_suppkey from {schema_name}.supplier where s_name='t' and "
        "s_address='a'"
    )
    assert actual_src_query == expected_src_query

    tgt_schema = [
        Schema("s_suppkey_t", "number"),
        Schema("s_name", "varchar"),
        Schema("s_address_t", "varchar"),
        Schema("s_nationkey", "number"),
        Schema("s_phone", "varchar"),
        Schema("s_acctbal", "number"),
        Schema("s_comment", "varchar"),
    ]

    actual_tgt_query = HashQueryBuilder(table_conf, tgt_schema, "target", "databricks").build_query()
    expected_tgt_query = (
        "select sha2(concat(coalesce(trim(s_suppkey_t),''), "
        'trim(s_address_t), trim(s_name)),256) as hash_value__recon, '
        "coalesce(trim(s_suppkey_t),'') as s_suppkey from {catalog_name}.{schema_name}.target_supplier where "
        "s_name='t' and s_address_t='a'"
    )

    assert actual_tgt_query == expected_tgt_query


def test_hash_query_builder_with_snowflake_source():
    table_conf = TestConf().get_table_conf_all_options
    schema = TestConf().get_schema
    alias_schema = TestConf().get_alias_schema
    actual_src_query = HashQueryBuilder(table_conf, schema, "source", "snowflake").build_query()
    expected_src_query = (
        "select sha2(concat(coalesce(trim(s_suppkey),''), trim(s_address), trim(s_name)),256) as hash_value__recon, "
        "coalesce(trim(s_nationkey),'') as s_nationkey,coalesce(trim(s_suppkey),'') as s_suppkey from {"
        "catalog_name}.{schema_name}.supplier where s_name='t' and s_address='a'"
    )
    assert actual_src_query == expected_src_query

    actual_tgt_query = HashQueryBuilder(table_conf, alias_schema, "target", "databricks").build_query()
    expected_tgt_query = (
        "select sha2(concat(coalesce(trim(s_suppkey_t),''), trim(s_address_t), trim(s_name)),"
        "256) as hash_value__recon, coalesce(trim(s_suppkey_t),'') as s_suppkey from {catalog_name}.{"
        "schema_name}.target_supplier where s_name='t' and s_address_t='a'"
    )

    assert actual_tgt_query == expected_tgt_query


def test_hash_query_builder_with_unsupported_source():
    table_conf = TestConf().get_table_conf_default
    schema = TestConf().get_schema
    query_builder = HashQueryBuilder(table_conf, schema, "source", "abc")

    with pytest.raises(Exception) as exc_info:
        query_builder.build_query()

    assert str(exc_info.value) == "Unsupported source type --> abc"
