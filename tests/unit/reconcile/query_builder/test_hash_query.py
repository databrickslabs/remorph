from databricks.labs.remorph.reconcile.dialects.utils import get_dialect
from databricks.labs.remorph.reconcile.query_builder.hash_query import HashQueryBuilder
from databricks.labs.remorph.reconcile.recon_config import Filters, ColumnMapping, Transformation, Layer


def test_hash_query_builder_for_snowflake_src(table_mapping_with_opts, table_schema):
    sch, sch_with_alias = table_schema
    src_actual = HashQueryBuilder(table_mapping_with_opts, sch, Layer.SOURCE, get_dialect("snowflake")).build_query(
        report_type="data"
    )
    src_expected = (
        "SELECT LOWER(SHA2(CONCAT(TRIM(s_address), TRIM(s_name), COALESCE(TRIM(s_nationkey), '_null_recon_'), "
        "TRIM(s_phone), COALESCE(TRIM(s_suppkey), '_null_recon_')), 256)) AS hash_value_recon, s_nationkey AS "
        "s_nationkey, "
        "s_suppkey AS s_suppkey FROM :tbl WHERE s_name = 't' AND s_address = 'a'"
    )

    tgt_actual = HashQueryBuilder(
        table_mapping_with_opts, sch_with_alias, Layer.TARGET, get_dialect("databricks")
    ).build_query(report_type="data")
    tgt_expected = (
        "SELECT LOWER(SHA2(CONCAT(TRIM(s_address_t), TRIM(s_name), COALESCE(TRIM(s_nationkey_t), '_null_recon_'), "
        "TRIM(s_phone_t), COALESCE(TRIM(s_suppkey_t), '_null_recon_')), 256)) AS hash_value_recon, s_nationkey_t AS "
        "s_nationkey, "
        "s_suppkey_t AS s_suppkey FROM :tbl WHERE s_name = 't' AND s_address_t = 'a'"
    )

    assert src_actual == src_expected
    assert tgt_actual == tgt_expected


def test_hash_query_builder_for_oracle_src(table_mapping_builder, table_schema, column_mapping):
    schema, _ = table_schema
    table_mapping = table_mapping_builder(
        join_columns=["s_suppkey", "s_nationkey"],
        filters=Filters(source="s_nationkey=1"),
        column_mapping=[ColumnMapping(source_name="s_nationkey", target_name="s_nationkey")],
    )
    src_actual = HashQueryBuilder(table_mapping, schema, Layer.SOURCE, get_dialect("oracle")).build_query(report_type="all")
    src_expected = (
        "SELECT LOWER(DBMS_CRYPTO.HASH(RAWTOHEX(COALESCE(TRIM(s_acctbal), '_null_recon_') || COALESCE(TRIM("
        "s_address), '_null_recon_') || "
        "COALESCE(TRIM(s_comment), '_null_recon_') || COALESCE(TRIM(s_name), '_null_recon_') || COALESCE(TRIM("
        "s_nationkey), '_null_recon_') || COALESCE(TRIM(s_phone), '_null_recon_') || COALESCE(TRIM(s_suppkey), "
        "'_null_recon_')), 2)) AS hash_value_recon, s_nationkey AS s_nationkey, "
        "s_suppkey AS s_suppkey FROM :tbl WHERE s_nationkey = 1"
    )

    tgt_actual = HashQueryBuilder(table_mapping, schema, Layer.TARGET, get_dialect("databricks")).build_query(
        report_type="all"
    )
    tgt_expected = (
        "SELECT LOWER(SHA2(CONCAT(COALESCE(TRIM(s_acctbal), '_null_recon_'), COALESCE(TRIM(s_address), "
        "'_null_recon_'), COALESCE(TRIM("
        "s_comment), '_null_recon_'), COALESCE(TRIM(s_name), '_null_recon_'), COALESCE(TRIM(s_nationkey), "
        "'_null_recon_'), COALESCE(TRIM(s_phone), "
        "'_null_recon_'), COALESCE(TRIM(s_suppkey), '_null_recon_')), 256)) AS hash_value_recon, s_nationkey AS "
        "s_nationkey, s_suppkey "
        "AS s_suppkey FROM :tbl"
    )

    assert src_actual == src_expected
    assert tgt_actual == tgt_expected


def test_hash_query_builder_for_databricks_src(table_mapping_builder, table_schema, column_mapping):
    table_mapping = table_mapping_builder(
        join_columns=["s_suppkey"],
        column_mapping=column_mapping,
        filters=Filters(target="s_nationkey_t=1"),
    )
    sch, sch_with_alias = table_schema
    src_actual = HashQueryBuilder(table_mapping, sch, Layer.SOURCE, get_dialect("databricks")).build_query(report_type="data")
    src_expected = (
        "SELECT LOWER(SHA2(CONCAT(COALESCE(TRIM(s_acctbal), '_null_recon_'), COALESCE(TRIM(s_address), '_null_recon_'), "
        "COALESCE(TRIM(s_comment), '_null_recon_'), COALESCE(TRIM(s_name), '_null_recon_'), COALESCE(TRIM("
        "s_nationkey), '_null_recon_'), COALESCE(TRIM("
        "s_phone), '_null_recon_'), COALESCE(TRIM(s_suppkey), '_null_recon_')), 256)) AS hash_value_recon, s_suppkey "
        "AS s_suppkey FROM :tbl"
    )

    tgt_actual = HashQueryBuilder(table_mapping, sch_with_alias, Layer.TARGET, get_dialect("databricks")).build_query(
        report_type="data"
    )
    tgt_expected = (
        "SELECT LOWER(SHA2(CONCAT(COALESCE(TRIM(s_acctbal_t), '_null_recon_'), COALESCE(TRIM(s_address_t), "
        "'_null_recon_'), COALESCE(TRIM("
        "s_comment_t), '_null_recon_'), COALESCE(TRIM(s_name), '_null_recon_'), COALESCE(TRIM(s_nationkey_t), "
        "'_null_recon_'), COALESCE(TRIM(s_phone_t), "
        "'_null_recon_'), COALESCE(TRIM(s_suppkey_t), '_null_recon_')), 256)) AS hash_value_recon, s_suppkey_t AS "
        "s_suppkey FROM :tbl WHERE "
        "s_nationkey_t = 1"
    )

    assert src_actual == src_expected
    assert tgt_actual == tgt_expected


def test_hash_query_builder_without_column_mapping(table_mapping_builder, table_schema):
    table_mapping = table_mapping_builder(
        join_columns=["s_suppkey"],
        filters=Filters(target="s_nationkey=1"),
    )
    sch, _ = table_schema
    src_actual = HashQueryBuilder(table_mapping, sch, Layer.SOURCE, get_dialect("databricks")).build_query(report_type="data")
    src_expected = (
        "SELECT LOWER(SHA2(CONCAT(COALESCE(TRIM(s_acctbal), '_null_recon_'), COALESCE(TRIM(s_address), '_null_recon_'),"
        " COALESCE(TRIM(s_comment), '_null_recon_'), COALESCE(TRIM(s_name), '_null_recon_'), COALESCE(TRIM("
        "s_nationkey), '_null_recon_'), COALESCE(TRIM("
        "s_phone), '_null_recon_'), COALESCE(TRIM(s_suppkey), '_null_recon_')), 256)) AS hash_value_recon, s_suppkey "
        "AS s_suppkey FROM :tbl"
    )

    tgt_actual = HashQueryBuilder(table_mapping, sch, Layer.TARGET, get_dialect("databricks")).build_query(report_type="data")
    tgt_expected = (
        "SELECT LOWER(SHA2(CONCAT(COALESCE(TRIM(s_acctbal), '_null_recon_'), COALESCE(TRIM(s_address), "
        "'_null_recon_'), COALESCE(TRIM("
        "s_comment), '_null_recon_'), COALESCE(TRIM(s_name), '_null_recon_'), COALESCE(TRIM(s_nationkey), "
        "'_null_recon_'), COALESCE(TRIM(s_phone), "
        "'_null_recon_'), COALESCE(TRIM(s_suppkey), '_null_recon_')), 256)) AS hash_value_recon, s_suppkey AS "
        "s_suppkey FROM :tbl WHERE "
        "s_nationkey = 1"
    )

    assert src_actual == src_expected
    assert tgt_actual == tgt_expected


def test_hash_query_builder_without_transformation(table_mapping_builder, table_schema, column_mapping):
    table_mapping = table_mapping_builder(
        join_columns=["s_suppkey"],
        transformations=[
            Transformation(column_name="s_address", source=None, target="trim(s_address_t)"),
            Transformation(column_name="s_name", source="trim(s_name)", target=None),
            Transformation(column_name="s_suppkey", source="trim(s_suppkey)", target=None),
        ],
        column_mapping=column_mapping,
        filters=Filters(target="s_nationkey_t=1"),
    )
    sch, tgt_sch = table_schema
    src_actual = HashQueryBuilder(table_mapping, sch, Layer.SOURCE, get_dialect("databricks")).build_query(report_type="data")
    src_expected = (
        "SELECT LOWER(SHA2(CONCAT(COALESCE(TRIM(s_acctbal), '_null_recon_'), s_address, "
        "COALESCE(TRIM(s_comment), '_null_recon_'), TRIM(s_name), COALESCE(TRIM(s_nationkey), '_null_recon_'), "
        "COALESCE(TRIM("
        "s_phone), '_null_recon_'), TRIM(s_suppkey)), 256)) AS hash_value_recon, TRIM(s_suppkey) AS s_suppkey FROM :tbl"
    )

    tgt_actual = HashQueryBuilder(table_mapping, tgt_sch, Layer.TARGET, get_dialect("databricks")).build_query(
        report_type="data"
    )
    tgt_expected = (
        "SELECT LOWER(SHA2(CONCAT(COALESCE(TRIM(s_acctbal_t), '_null_recon_'), TRIM(s_address_t), COALESCE(TRIM("
        "s_comment_t), '_null_recon_'), s_name, COALESCE(TRIM(s_nationkey_t), '_null_recon_'), COALESCE(TRIM("
        "s_phone_t), "
        "'_null_recon_'), s_suppkey_t), 256)) AS hash_value_recon, s_suppkey_t AS s_suppkey FROM :tbl WHERE "
        "s_nationkey_t = 1"
    )

    assert src_actual == src_expected
    assert tgt_actual == tgt_expected


def test_hash_query_builder_for_report_type_is_row(table_mapping_with_opts, table_schema, column_mapping):
    sch, sch_with_alias = table_schema
    src_actual = HashQueryBuilder(table_mapping_with_opts, sch, Layer.SOURCE, get_dialect("databricks")).build_query(
        report_type="row"
    )
    src_expected = (
        "SELECT LOWER(SHA2(CONCAT(TRIM(s_address), TRIM(s_name), COALESCE(TRIM(s_nationkey), '_null_recon_'), "
        "TRIM(s_phone), COALESCE(TRIM(s_suppkey), '_null_recon_')), 256)) AS hash_value_recon, TRIM(s_address) AS "
        "s_address, TRIM(s_name) AS s_name, s_nationkey AS s_nationkey, TRIM(s_phone) "
        "AS s_phone, s_suppkey AS s_suppkey FROM :tbl WHERE s_name = 't' AND "
        "s_address = 'a'"
    )

    tgt_actual = HashQueryBuilder(
        table_mapping_with_opts, sch_with_alias, Layer.TARGET, get_dialect("databricks")
    ).build_query(report_type="row")
    tgt_expected = (
        "SELECT LOWER(SHA2(CONCAT(TRIM(s_address_t), TRIM(s_name), COALESCE(TRIM(s_nationkey_t), '_null_recon_'), "
        "TRIM(s_phone_t), COALESCE(TRIM(s_suppkey_t), '_null_recon_')), 256)) AS hash_value_recon, TRIM(s_address_t) "
        "AS s_address, TRIM(s_name) AS s_name, s_nationkey_t AS s_nationkey, "
        "TRIM(s_phone_t) AS s_phone, s_suppkey_t AS s_suppkey FROM :tbl WHERE s_name "
        "= 't' AND s_address_t = 'a'"
    )

    assert src_actual == src_expected
    assert tgt_actual == tgt_expected


def test_config_case_sensitivity(table_mapping_builder, table_schema, column_mapping):
    table_mapping = table_mapping_builder(
        select_columns=["S_SUPPKEY", "S_name", "S_ADDRESS", "S_NATIOnKEY", "S_PhONE", "S_acctbal"],
        drop_columns=["s_Comment"],
        join_columns=["S_SUPPKEY"],
        transformations=[
            Transformation(column_name="S_ADDRESS", source=None, target="trim(s_address_t)"),
            Transformation(column_name="S_NAME", source="trim(s_name)", target=None),
            Transformation(column_name="s_suppKey", source="trim(s_suppkey)", target=None),
        ],
        column_mapping=column_mapping,
        filters=Filters(target="s_nationkey_t=1"),
    )
    sch, tgt_sch = table_schema
    src_actual = HashQueryBuilder(table_mapping, sch, Layer.SOURCE, get_dialect("databricks")).build_query(report_type="data")
    src_expected = (
        "SELECT LOWER(SHA2(CONCAT(COALESCE(TRIM(s_acctbal), '_null_recon_'), s_address, "
        "TRIM(s_name), COALESCE(TRIM(s_nationkey), '_null_recon_'), COALESCE(TRIM("
        "s_phone), '_null_recon_'), TRIM(s_suppkey)), 256)) AS hash_value_recon, TRIM(s_suppkey) AS s_suppkey FROM :tbl"
    )

    tgt_actual = HashQueryBuilder(table_mapping, tgt_sch, Layer.TARGET, get_dialect("databricks")).build_query(
        report_type="data"
    )
    tgt_expected = (
        "SELECT LOWER(SHA2(CONCAT(COALESCE(TRIM(s_acctbal_t), '_null_recon_'), TRIM(s_address_t), s_name, "
        "COALESCE(TRIM("
        "s_nationkey_t), '_null_recon_'), COALESCE(TRIM(s_phone_t), '_null_recon_'), s_suppkey_t), "
        "256)) AS hash_value_recon, s_suppkey_t AS "
        "s_suppkey FROM :tbl WHERE s_nationkey_t = 1"
    )

    assert src_actual == src_expected
    assert tgt_actual == tgt_expected
