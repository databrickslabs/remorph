import pytest

from databricks.labs.lakebridge.reconcile.query_builder.query_builder import QueryBuilder
from databricks.labs.lakebridge.reconcile.recon_config import Filters, ColumnMapping, Transformation, Layer

_test_config_1 = {
    "join_columns": ["s_suppkey", "s_nationkey"],
    "filters": Filters(source="s_nationkey = 1"),
    "column_mapping": [ColumnMapping(source_name="s_nationkey", target_name="s_nationkey")],
}

_test_config_2 = {
    "join_columns": ["s_suppkey"],
    "filters": Filters(target="s_nationkey_t = 1"),
}

_test_config_3 = {
    "join_columns": ["s_suppkey"],
    "column_mapping": [],
    "filters": Filters(target="s_nationkey = 1"),
}

_test_config_4 = {
    "join_columns": ["s_suppkey"],
    "transformations": [
        Transformation(column_name="s_address", source=None, target="TRIM(s_address_t)"),
        Transformation(column_name="s_name", source="TRIM(s_name)", target=None),
        Transformation(column_name="s_suppkey", source="TRIM(s_suppkey)", target=None),
    ],
    "filters": Filters(target="s_nationkey_t = 1"),
}

_test_config_5 = {
    "select_columns": ["S_SUPPKEY", "S_name", "S_ADDRESS", "S_NATIOnKEY", "S_PhONE", "S_acctbal"],
    "drop_columns": ["s_Comment"],
    "join_columns": ["S_SUPPKEY"],
    "transformations": [
        Transformation(column_name="S_ADDRESS", source=None, target="TRIM(s_address_t)"),
        Transformation(column_name="S_NAME", source="TRIM(s_name)", target=None),
        Transformation(column_name="s_suppKey", source="TRIM(s_suppkey)", target=None),
    ],
    "filters": Filters(target="s_nationkey_t = 1"),
}


@pytest.mark.parametrize(
    "config, column_types, layer, report_type, dialect, expected",
    [
        (
            None,
            "src_column_types",
            Layer.SOURCE,
            "data",
            "snowflake",
            "SELECT LOWER(SHA2(CONCAT("
            "TRIM(s_address),"
            " TRIM(s_name),"
            " COALESCE(TRIM(s_nationkey), '_null_recon_'),"
            " TRIM(s_phone),"
            " COALESCE(TRIM(s_suppkey), '_null_recon_')), 256))"
            ""
            " AS hash_value_recon, s_nationkey,"
            " s_suppkey FROM :tbl WHERE s_name = 't' AND s_address = 'a'",
        ),
        (
            None,
            "tgt_column_types",
            Layer.TARGET,
            "data",
            "databricks",
            "SELECT LOWER(SHA2(CONCAT("
            "TRIM(s_address_t),"
            " TRIM(s_name),"
            " COALESCE(TRIM(s_nationkey_t), '_null_recon_'),"
            " TRIM(s_phone_t),"
            " COALESCE(TRIM(s_suppkey_t), '_null_recon_')), 256))"
            " AS hash_value_recon,"
            " s_nationkey_t AS s_nationkey,"
            " s_suppkey_t AS s_suppkey"
            " FROM :tbl WHERE s_name = 't' AND s_address_t = 'a'",
        ),
        (
            _test_config_1,
            "src_column_types",
            Layer.SOURCE,
            "all",
            "oracle",
            "SELECT LOWER(DBMS_CRYPTO.HASH(RAWTOHEX("
            "COALESCE(TRIM(s_acctbal), '_null_recon_')"
            " || COALESCE(TRIM(s_address), '_null_recon_')"
            " || COALESCE(TRIM(s_comment), '_null_recon_')"
            " || COALESCE(TRIM(s_name), '_null_recon_')"
            " || COALESCE(TRIM(s_nationkey), '_null_recon_')"
            " || COALESCE(TRIM(s_phone), '_null_recon_')"
            " || COALESCE(TRIM(s_suppkey), '_null_recon_')), 2))"
            " AS hash_value_recon,"
            " s_nationkey,"
            " s_suppkey"
            " FROM :tbl WHERE s_nationkey = 1",
        ),
        (
            _test_config_1,
            "src_column_types",
            Layer.TARGET,
            "all",
            "databricks",
            "SELECT LOWER(SHA2(CONCAT("
            "COALESCE(TRIM(s_acctbal), '_null_recon_'),"
            " COALESCE(TRIM(s_address), '_null_recon_'),"
            " COALESCE(TRIM(s_comment), '_null_recon_'),"
            " COALESCE(TRIM(s_name), '_null_recon_'),"
            " COALESCE(TRIM(s_nationkey), '_null_recon_'),"
            " COALESCE(TRIM(s_phone), '_null_recon_'),"
            " COALESCE(TRIM(s_suppkey), '_null_recon_')), 256))"
            " AS hash_value_recon,"
            ""
            " s_nationkey,"
            " s_suppkey"
            " FROM :tbl",
        ),
        (
            _test_config_2,
            "src_column_types",
            Layer.SOURCE,
            "data",
            "databricks",
            "SELECT LOWER(SHA2(CONCAT("
            "COALESCE(TRIM(s_acctbal), '_null_recon_'),"
            " COALESCE(TRIM(s_address), '_null_recon_'),"
            " COALESCE(TRIM(s_comment), '_null_recon_'),"
            " COALESCE(TRIM(s_name), '_null_recon_'),"
            " COALESCE(TRIM(s_nationkey), '_null_recon_'),"
            " COALESCE(TRIM(s_phone), '_null_recon_'),"
            " COALESCE(TRIM(s_suppkey), '_null_recon_')), 256))"
            " AS hash_value_recon,"
            " s_suppkey FROM :tbl",
        ),
        (
            _test_config_2,
            "tgt_column_types",
            Layer.TARGET,
            "data",
            "databricks",
            "SELECT LOWER(SHA2(CONCAT("
            "COALESCE(TRIM(s_acctbal_t), '_null_recon_'),"
            " COALESCE(TRIM(s_address_t), '_null_recon_'),"
            " COALESCE(TRIM(s_comment_t), '_null_recon_'),"
            " COALESCE(TRIM(s_name), '_null_recon_'),"
            " COALESCE(TRIM(s_nationkey_t), '_null_recon_'),"
            " COALESCE(TRIM(s_phone_t), '_null_recon_'),"
            " COALESCE(TRIM(s_suppkey_t), '_null_recon_')), 256))"
            " AS hash_value_recon,"
            " s_suppkey_t AS s_suppkey"
            " FROM :tbl WHERE s_nationkey_t = 1",
        ),
        (
            _test_config_3,
            "src_column_types",
            Layer.SOURCE,
            "data",
            "databricks",
            "SELECT LOWER(SHA2(CONCAT("
            "COALESCE(TRIM(s_acctbal), '_null_recon_'),"
            " COALESCE(TRIM(s_address), '_null_recon_'),"
            " COALESCE(TRIM(s_comment), '_null_recon_'),"
            " COALESCE(TRIM(s_name), '_null_recon_'),"
            " COALESCE(TRIM(s_nationkey), '_null_recon_'),"
            " COALESCE(TRIM(s_phone), '_null_recon_'),"
            " COALESCE(TRIM(s_suppkey), '_null_recon_')), 256))"
            " AS hash_value_recon,"
            " s_suppkey FROM :tbl",
        ),
        (
            _test_config_3,
            "src_column_types",
            Layer.TARGET,
            "data",
            "databricks",
            "SELECT LOWER(SHA2(CONCAT("
            "COALESCE(TRIM(s_acctbal), '_null_recon_'),"
            " COALESCE(TRIM(s_address), '_null_recon_'),"
            " COALESCE(TRIM(s_comment), '_null_recon_'),"
            " COALESCE(TRIM(s_name), '_null_recon_'),"
            " COALESCE(TRIM(s_nationkey), '_null_recon_'),"
            " COALESCE(TRIM(s_phone), '_null_recon_'),"
            " COALESCE(TRIM(s_suppkey), '_null_recon_')), 256))"
            " AS hash_value_recon,"
            " s_suppkey FROM :tbl WHERE s_nationkey = 1",
        ),
        (
            _test_config_4,
            "src_column_types",
            Layer.SOURCE,
            "data",
            "databricks",
            "SELECT LOWER(SHA2(CONCAT("
            "COALESCE(TRIM(s_acctbal), '_null_recon_'),"
            ""
            " s_address,"
            " COALESCE(TRIM(s_comment), '_null_recon_'),"
            " TRIM(s_name),"
            " COALESCE(TRIM(s_nationkey), '_null_recon_'),"
            " COALESCE(TRIM(s_phone), '_null_recon_'),"
            " TRIM(s_suppkey)), 256)) AS hash_value_recon,"
            " TRIM(s_suppkey) AS s_suppkey"
            " FROM :tbl",
        ),
        (
            _test_config_4,
            "tgt_column_types",
            Layer.TARGET,
            "data",
            "databricks",
            "SELECT LOWER(SHA2(CONCAT("
            "COALESCE(TRIM(s_acctbal_t), '_null_recon_'),"
            " TRIM(s_address_t),"
            " COALESCE(TRIM(s_comment_t), '_null_recon_'),"
            " s_name,"
            " COALESCE(TRIM(s_nationkey_t), '_null_recon_'),"
            " COALESCE(TRIM(s_phone_t), '_null_recon_'),"
            " s_suppkey_t), 256)) AS hash_value_recon,"
            " s_suppkey_t AS s_suppkey"
            " FROM :tbl WHERE s_nationkey_t = 1",
        ),
        (
            None,
            "src_column_types",
            Layer.SOURCE,
            "row",
            "databricks",
            "SELECT LOWER(SHA2(CONCAT("
            "TRIM(s_address),"
            " TRIM(s_name),"
            " COALESCE(TRIM(s_nationkey), '_null_recon_'),"
            " TRIM(s_phone),"
            " COALESCE(TRIM(s_suppkey), '_null_recon_')), 256)) AS hash_value_recon,"
            " TRIM(s_address) AS s_address,"
            " TRIM(s_name) AS s_name,"
            " s_nationkey,"
            " TRIM(s_phone) AS s_phone,"
            " s_suppkey"
            " FROM :tbl WHERE s_name = 't' AND s_address = 'a'",
        ),
        (
            None,
            "tgt_column_types",
            Layer.TARGET,
            "row",
            "databricks",
            "SELECT LOWER(SHA2(CONCAT("
            "TRIM(s_address_t),"
            " TRIM(s_name),"
            " COALESCE(TRIM(s_nationkey_t), '_null_recon_'),"
            " TRIM(s_phone_t),"
            " COALESCE(TRIM(s_suppkey_t), '_null_recon_')), 256)) AS hash_value_recon,"
            " TRIM(s_address_t) AS s_address,"
            " TRIM(s_name) AS s_name,"
            " s_nationkey_t AS s_nationkey,"
            " TRIM(s_phone_t) AS s_phone,"
            " s_suppkey_t AS s_suppkey"
            " FROM :tbl WHERE s_name = 't' AND s_address_t = 'a'",
        ),
        (
            _test_config_5,
            "src_column_types",
            Layer.SOURCE,
            "data",
            "databricks",
            "SELECT LOWER(SHA2(CONCAT("
            "COALESCE(TRIM(s_acctbal), '_null_recon_'),"
            " s_address,"
            " TRIM(s_name),"
            " COALESCE(TRIM(s_nationkey), '_null_recon_'),"
            " COALESCE(TRIM(s_phone), '_null_recon_'),"
            " TRIM(s_suppkey)), 256)) AS hash_value_recon,"
            " TRIM(s_suppkey) AS s_suppkey FROM :tbl",
        ),
        (
            _test_config_5,
            "tgt_column_types",
            Layer.TARGET,
            "data",
            "databricks",
            "SELECT LOWER(SHA2(CONCAT("
            "COALESCE(TRIM(s_acctbal_t), '_null_recon_'),"
            " TRIM(s_address_t),"
            " s_name,"
            " COALESCE(TRIM(s_nationkey_t), '_null_recon_'),"
            " COALESCE(TRIM(s_phone_t), '_null_recon_'),"
            " s_suppkey_t), 256)) AS hash_value_recon,"
            " s_suppkey_t AS s_suppkey"
            " FROM :tbl WHERE s_nationkey_t = 1",
        ),
    ],
)
def test_hash_query_builder(
    config,
    column_types,
    layer,
    report_type,
    dialect,
    expected,
    table_mapping_factory,
    table_mapping_with_opts,
    column_mapping,
    request,
):
    if config is None:
        mapping = table_mapping_with_opts
    else:
        if config.get("column_mapping", None) is None:
            config["column_mapping"] = column_mapping
        mapping = table_mapping_factory(**config)
    col_types = request.getfixturevalue(column_types)
    builder = QueryBuilder.for_dialect(mapping, col_types, layer, dialect)
    query = builder.build_hash_query(report_type=report_type)
    assert query == expected
