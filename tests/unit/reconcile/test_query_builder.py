from databricks.labs.remorph.reconcile.query_builder import QueryBuilder
from databricks.labs.remorph.reconcile.recon_config import (
    ColumnMapping,
    JdbcReaderOptions,
    JoinColumns,
    Schema,
    Tables,
    Thresholds,
    Transformation,
)


def test_query_builder_without_join_column():
    table_conf = Tables(
        source_name="supplier",
        target_name="supplier",
        jdbc_reader_options=None,
        join_columns=None,
        select_columns=None,
        drop_columns=None,
        column_mapping=None,
        transformations=None,
        thresholds=None,
        filters=None,
    )
    src_schema = [
        Schema("s_suppkey", "number"),
        Schema("s_name", "varchar"),
        Schema("s_address", "varchar"),
        Schema("s_nationkey", "number"),
        Schema("s_phone", "varchar"),
        Schema("s_acctbal", "number"),
        Schema("s_comment", "varchar"),
    ]

    actual_src_query = QueryBuilder(table_conf, src_schema, "source", "oracle").build_hash_query()
    expected_src_query = (
        "select lower(RAWTOHEX(STANDARD_HASH(coalesce(trim(s_acctbal),'') || "
        "coalesce(trim(s_address),'') || coalesce(trim(s_comment),'') || "
        "coalesce(trim(s_name),'') || coalesce(trim(s_nationkey),'') || "
        "coalesce(trim(s_phone),'') || coalesce(trim(s_suppkey),''), 'SHA256'))) as "
        "hash_value__recon from supplier "
        "where  1 = 1 "
    )
    assert actual_src_query == expected_src_query

    tgt_schema = [
        Schema("s_suppkey", "number"),
        Schema("s_name", "varchar"),
        Schema("s_address", "varchar"),
        Schema("s_nationkey", "number"),
        Schema("s_phone", "varchar"),
        Schema("s_acctbal", "number"),
        Schema("s_comment", "varchar"),
    ]

    actual_tgt_query = QueryBuilder(table_conf, tgt_schema, "target", "databricks").build_hash_query()
    expected_tgt_query = (
        "select sha2(concat(coalesce(trim(s_acctbal),''), "
        "coalesce(trim(s_address),''), coalesce(trim(s_comment),''), "
        "coalesce(trim(s_name),''), coalesce(trim(s_nationkey),''), "
        "coalesce(trim(s_phone),''), coalesce(trim(s_suppkey),'')),256) as "
        "hash_value__recon from supplier "
        "where  1 = 1 "
    )
    assert actual_tgt_query == expected_tgt_query


def test_query_builder_with_defaults():
    table_conf = Tables(
        source_name="supplier",
        target_name="supplier",
        jdbc_reader_options=None,
        join_columns=[JoinColumns(source_name="s_suppkey", target_name="s_suppkey")],
        select_columns=None,
        drop_columns=None,
        column_mapping=None,
        transformations=None,
        thresholds=None,
        filters=None,
    )
    src_schema = [
        Schema("s_suppkey", "number"),
        Schema("s_name", "varchar"),
        Schema("s_address", "varchar"),
        Schema("s_nationkey", "number"),
        Schema("s_phone", "varchar"),
        Schema("s_acctbal", "number"),
        Schema("s_comment", "varchar"),
    ]

    actual_src_query = QueryBuilder(table_conf, src_schema, "source", "oracle").build_hash_query()
    expected_src_query = (
        "select lower(RAWTOHEX(STANDARD_HASH(coalesce(trim(s_acctbal),'') || "
        "coalesce(trim(s_address),'') || coalesce(trim(s_comment),'') || "
        "coalesce(trim(s_name),'') || coalesce(trim(s_nationkey),'') || "
        "coalesce(trim(s_phone),'') || coalesce(trim(s_suppkey),''), 'SHA256'))) as "
        "hash_value__recon, coalesce(trim(s_suppkey),'') as s_suppkey from supplier "
        "where  1 = 1 "
    )
    assert actual_src_query == expected_src_query

    tgt_schema = [
        Schema("s_suppkey", "number"),
        Schema("s_name", "varchar"),
        Schema("s_address", "varchar"),
        Schema("s_nationkey", "number"),
        Schema("s_phone", "varchar"),
        Schema("s_acctbal", "number"),
        Schema("s_comment", "varchar"),
    ]

    actual_tgt_query = QueryBuilder(table_conf, tgt_schema, "target", "databricks").build_hash_query()
    expected_tgt_query = (
        "select sha2(concat(coalesce(trim(s_acctbal),''), "
        "coalesce(trim(s_address),''), coalesce(trim(s_comment),''), "
        "coalesce(trim(s_name),''), coalesce(trim(s_nationkey),''), "
        "coalesce(trim(s_phone),''), coalesce(trim(s_suppkey),'')),256) as "
        "hash_value__recon, coalesce(trim(s_suppkey),'') as s_suppkey from supplier "
        "where  1 = 1 "
    )
    assert actual_tgt_query == expected_tgt_query


def test_query_builder_with_select():
    table_conf = Tables(
        source_name="supplier",
        target_name="supplier",
        jdbc_reader_options=None,
        join_columns=[JoinColumns(source_name="s_suppkey", target_name="s_suppkey_t")],
        select_columns=["s_suppkey", "s_name", "s_address"],
        drop_columns=None,
        column_mapping=[
            ColumnMapping(source_name="s_suppkey", target_name="s_suppkey_t"),
            ColumnMapping(source_name="s_address", target_name="s_address_t"),
        ],
        transformations=None,
        thresholds=None,
        filters=None,
    )
    src_schema = [
        Schema("s_suppkey", "number"),
        Schema("s_name", "varchar"),
        Schema("s_address", "varchar"),
        Schema("s_nationkey", "number"),
        Schema("s_phone", "varchar"),
        Schema("s_acctbal", "number"),
        Schema("s_comment", "varchar"),
    ]

    actual_src_query = QueryBuilder(table_conf, src_schema, "source", "oracle").build_hash_query()
    expected_src_query = (
        "select lower(RAWTOHEX(STANDARD_HASH(coalesce(trim(s_address),'') || "
        "coalesce(trim(s_name),'') || coalesce(trim(s_suppkey),''), 'SHA256'))) as "
        "hash_value__recon, coalesce(trim(s_suppkey),'') as s_suppkey from supplier "
        "where  1 = 1 "
    )
    assert actual_src_query == expected_src_query

    tgt_schema = [
        Schema("s_suppkey_t", "number"),
        Schema("s_name", "varchar"),
        Schema("s_address_t", "varchar"),
        Schema("s_nationkey_t", "number"),
        Schema("s_phone_t", "varchar"),
        Schema("s_acctbal_t", "number"),
        Schema("s_comment_t", "varchar"),
    ]

    actual_tgt_query = QueryBuilder(table_conf, tgt_schema, "target", "databricks").build_hash_query()
    expected_tgt_query = (
        "select sha2(concat(coalesce(trim(s_address_t),''), "
        "coalesce(trim(s_name),''), coalesce(trim(s_suppkey_t),'')),256) as "
        "hash_value__recon, coalesce(trim(s_suppkey_t),'') as s_suppkey from supplier "
        "where  1 = 1 "
    )

    assert actual_tgt_query == expected_tgt_query


def test_query_builder_with_transformations_with_drop_and_default_select():
    table_conf = Tables(
        source_name="supplier",
        target_name="supplier",
        jdbc_reader_options=None,
        join_columns=[JoinColumns(source_name="s_suppkey", target_name="s_suppkey_t")],
        select_columns=None,
        drop_columns=["s_comment"],
        column_mapping=[
            ColumnMapping(source_name="s_suppkey", target_name="s_suppkey_t"),
            ColumnMapping(source_name="s_address", target_name="s_address_t"),
            ColumnMapping(source_name="s_nationkey", target_name="s_nationkey_t"),
            ColumnMapping(source_name="s_phone", target_name="s_phone_t"),
            ColumnMapping(source_name="s_acctbal", target_name="s_acctbal_t"),
            ColumnMapping(source_name="s_comment", target_name="s_comment_t"),
        ],
        transformations=[
            Transformation(column_name="s_address", source="trim(s_address)", target="trim(s_address_t)"),
            Transformation(column_name="s_phone", source="trim(s_phone)", target="trim(s_phone_t)"),
            Transformation(column_name="s_name", source="trim(s_name)", target="trim(s_name)"),
            Transformation(
                column_name="s_acctbal",
                source="trim(to_char(s_acctbal_t, '9999999999.99'))",
                target="cast(s_acctbal_t as decimal(38,2))",
            ),
        ],
        thresholds=None,
        filters=None,
    )
    src_schema = [
        Schema("s_suppkey", "number"),
        Schema("s_name", "varchar"),
        Schema("s_address", "varchar"),
        Schema("s_nationkey", "number"),
        Schema("s_phone", "varchar"),
        Schema("s_acctbal", "number"),
        Schema("s_comment", "varchar"),
    ]

    actual_src_query = QueryBuilder(table_conf, src_schema, "source", "oracle").build_hash_query()
    expected_src_query = (
        'select lower(RAWTOHEX(STANDARD_HASH(trim(to_char(s_acctbal_t, '
        "'9999999999.99')) || trim(s_address) || trim(s_name) || "
        "coalesce(trim(s_nationkey),'') || trim(s_phone) || "
        "coalesce(trim(s_suppkey),''), 'SHA256'))) as hash_value__recon, "
        "coalesce(trim(s_suppkey),'') as s_suppkey from supplier where  1 = 1 "
    )
    assert actual_src_query == expected_src_query

    tgt_schema = [
        Schema("s_suppkey_t", "number"),
        Schema("s_name", "varchar"),
        Schema("s_address_t", "varchar"),
        Schema("s_nationkey_t", "number"),
        Schema("s_phone_t", "varchar"),
        Schema("s_acctbal_t", "number"),
        Schema("s_comment_t", "varchar"),
    ]

    actual_tgt_query = QueryBuilder(table_conf, tgt_schema, "target", "databricks").build_hash_query()
    expected_tgt_query = (
        'select sha2(concat(cast(s_acctbal_t as decimal(38,2)), trim(s_address_t), '
        "trim(s_name), coalesce(trim(s_nationkey_t),''), "
        "trim(s_phone_t), coalesce(trim(s_suppkey_t),'')),256) as "
        "hash_value__recon, coalesce(trim(s_suppkey_t),'') as s_suppkey from supplier "
        'where  1 = 1 '
    )

    assert actual_tgt_query == expected_tgt_query


def test_query_builder_with_jdbc_reader_options():
    table_conf = Tables(
        source_name="supplier",
        target_name="supplier",
        jdbc_reader_options=JdbcReaderOptions(
            number_partitions=100, partition_column="s_nationkey", lower_bound="0", upper_bound="100"
        ),
        join_columns=[JoinColumns(source_name="s_suppkey", target_name="s_suppkey_t")],
        select_columns=["s_suppkey", "s_name", "s_address"],
        drop_columns=None,
        column_mapping=[
            ColumnMapping(source_name="s_suppkey", target_name="s_suppkey_t"),
            ColumnMapping(source_name="s_address", target_name="s_address_t"),
        ],
        transformations=None,
        thresholds=None,
        filters=None,
    )
    src_schema = [
        Schema("s_suppkey", "number"),
        Schema("s_name", "varchar"),
        Schema("s_address", "varchar"),
        Schema("s_nationkey", "number"),
        Schema("s_phone", "varchar"),
        Schema("s_acctbal", "number"),
        Schema("s_comment", "varchar"),
    ]

    actual_src_query = QueryBuilder(table_conf, src_schema, "source", "oracle").build_hash_query()
    expected_src_query = (
        "select lower(RAWTOHEX(STANDARD_HASH(coalesce(trim(s_address),'') || "
        "coalesce(trim(s_name),'') || coalesce(trim(s_suppkey),''), 'SHA256'))) as "
        "hash_value__recon, coalesce(trim(s_nationkey),'') as s_nationkey,coalesce(trim(s_suppkey),'') as s_suppkey "
        "from supplier "
        "where  1 = 1 "
    )

    assert actual_src_query == expected_src_query

    tgt_schema = [
        Schema("s_suppkey_t", "number"),
        Schema("s_name", "varchar"),
        Schema("s_address_t", "varchar"),
        Schema("s_nationkey_t", "number"),
        Schema("s_phone_t", "varchar"),
        Schema("s_acctbal_t", "number"),
        Schema("s_comment_t", "varchar"),
    ]

    actual_tgt_query = QueryBuilder(table_conf, tgt_schema, "target", "databricks").build_hash_query()
    expected_tgt_query = (
        "select sha2(concat(coalesce(trim(s_address_t),''), "
        "coalesce(trim(s_name),''), coalesce(trim(s_suppkey_t),'')),256) as "
        "hash_value__recon, coalesce(trim(s_suppkey_t),'') as s_suppkey from supplier "
        "where  1 = 1 "
    )

    assert actual_tgt_query == expected_tgt_query


def test_query_builder_with_threshold():
    table_conf = Tables(
        source_name="supplier",
        target_name="supplier",
        jdbc_reader_options=JdbcReaderOptions(
            number_partitions=100, partition_column="s_nationkey", lower_bound="0", upper_bound="100"
        ),
        join_columns=[JoinColumns(source_name="s_suppkey", target_name="s_suppkey_t")],
        select_columns=None,
        drop_columns=None,
        column_mapping=[
            ColumnMapping(source_name="s_suppkey", target_name="s_suppkey_t"),
            ColumnMapping(source_name="s_address", target_name="s_address_t"),
        ],
        transformations=[
            Transformation(column_name="s_address", source="trim(s_address)", target="trim(s_address_t)"),
            Transformation(column_name="s_phone", source="trim(s_phone)", target="trim(s_phone)"),
            Transformation(column_name="s_name", source="trim(s_name)", target="trim(s_name)"),
        ],
        thresholds=[Thresholds(column_name="s_acctbal", lower_bound="0", upper_bound="100", type="int")],
        filters=None,
    )
    src_schema = [
        Schema("s_suppkey", "number"),
        Schema("s_name", "varchar"),
        Schema("s_address", "varchar"),
        Schema("s_nationkey", "number"),
        Schema("s_phone", "varchar"),
        Schema("s_acctbal", "number"),
        Schema("s_comment", "varchar"),
    ]

    actual_src_query = QueryBuilder(table_conf, src_schema, "source", "oracle").build_hash_query()
    expected_src_query = (
        'select lower(RAWTOHEX(STANDARD_HASH(trim(s_address) || '
        "coalesce(trim(s_comment),'') || trim(s_name) || "
        "coalesce(trim(s_nationkey),'') || trim(s_phone) || "
        "coalesce(trim(s_suppkey),''), 'SHA256'))) as hash_value__recon, "
        "coalesce(trim(s_nationkey),'') as s_nationkey,coalesce(trim(s_suppkey),'') "
        'as s_suppkey from supplier where  1 = 1 '
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

    actual_tgt_query = QueryBuilder(table_conf, tgt_schema, "target", "databricks").build_hash_query()
    expected_tgt_query = (
        "select sha2(concat(trim(s_address_t), coalesce(trim(s_comment),''), "
        "trim(s_name), coalesce(trim(s_nationkey),''), trim(s_phone), "
        "coalesce(trim(s_suppkey_t),'')),256) as hash_value__recon, "
        "coalesce(trim(s_suppkey_t),'') as s_suppkey from supplier where  1 = 1 "
    )

    assert actual_tgt_query == expected_tgt_query
