import pytest

from databricks.labs.remorph.reconcile.query_builder import (
    HashQueryBuilder,
    ThresholdQueryBuilder,
)
from databricks.labs.remorph.reconcile.query_config import QueryConfig
from databricks.labs.remorph.reconcile.recon_config import (
    ColumnMapping,
    Filters,
    JdbcReaderOptions,
    Schema,
    Table,
    Thresholds,
    Transformation,
)


def test_hash_query_builder_without_join_column():
    table_conf = Table(
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

    src_qrc = QueryConfig(table_conf, src_schema, "source", "oracle")
    actual_src_query = HashQueryBuilder(src_qrc).build_query()
    expected_src_query = (
        "select lower(RAWTOHEX(STANDARD_HASH(coalesce(trim(s_acctbal),'') || "
        "coalesce(trim(s_address),'') || coalesce(trim(s_comment),'') || "
        "coalesce(trim(s_name),'') || coalesce(trim(s_nationkey),'') || "
        "coalesce(trim(s_phone),'') || coalesce(trim(s_suppkey),''), 'SHA256'))) as "
        "hash_value__recon from {schema_name}.supplier "
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

    tgt_qrc = QueryConfig(table_conf, tgt_schema, "target", "databricks")
    actual_tgt_query = HashQueryBuilder(tgt_qrc).build_query()
    expected_tgt_query = (
        "select sha2(concat(coalesce(trim(s_acctbal),''), "
        "coalesce(trim(s_address),''), coalesce(trim(s_comment),''), "
        "coalesce(trim(s_name),''), coalesce(trim(s_nationkey),''), "
        "coalesce(trim(s_phone),''), coalesce(trim(s_suppkey),'')),256) as "
        "hash_value__recon from {catalog_name}.{schema_name}.supplier "
        "where  1 = 1 "
    )
    assert actual_tgt_query == expected_tgt_query


def test_hash_query_builder_with_defaults():
    table_conf = Table(
        source_name="supplier",
        target_name="supplier",
        jdbc_reader_options=None,
        join_columns=["s_suppkey"],
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

    src_qrc = QueryConfig(table_conf, src_schema, "source", "oracle")
    actual_src_query = HashQueryBuilder(src_qrc).build_query()
    expected_src_query = (
        "select lower(RAWTOHEX(STANDARD_HASH(coalesce(trim(s_acctbal),'') || "
        "coalesce(trim(s_address),'') || coalesce(trim(s_comment),'') || "
        "coalesce(trim(s_name),'') || coalesce(trim(s_nationkey),'') || "
        "coalesce(trim(s_phone),'') || coalesce(trim(s_suppkey),''), 'SHA256'))) as "
        "hash_value__recon, coalesce(trim(s_suppkey),'') as s_suppkey from {schema_name}.supplier "
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

    tgt_qrc = QueryConfig(table_conf, tgt_schema, "target", "databricks")
    actual_tgt_query = HashQueryBuilder(tgt_qrc).build_query()
    expected_tgt_query = (
        "select sha2(concat(coalesce(trim(s_acctbal),''), "
        "coalesce(trim(s_address),''), coalesce(trim(s_comment),''), "
        "coalesce(trim(s_name),''), coalesce(trim(s_nationkey),''), "
        "coalesce(trim(s_phone),''), coalesce(trim(s_suppkey),'')),256) as "
        "hash_value__recon, coalesce(trim(s_suppkey),'') as s_suppkey from {catalog_name}.{schema_name}.supplier "
        "where  1 = 1 "
    )
    assert actual_tgt_query == expected_tgt_query


def test_hash_query_builder_with_select():
    table_conf = Table(
        source_name="supplier",
        target_name="supplier",
        jdbc_reader_options=None,
        join_columns=["s_suppkey"],
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

    src_qrc = QueryConfig(table_conf, src_schema, "source", "oracle")
    actual_src_query = HashQueryBuilder(src_qrc).build_query()
    expected_src_query = (
        "select lower(RAWTOHEX(STANDARD_HASH(coalesce(trim(s_address),'') || "
        "coalesce(trim(s_name),'') || coalesce(trim(s_suppkey),''), 'SHA256'))) as "
        "hash_value__recon, coalesce(trim(s_suppkey),'') as s_suppkey from {schema_name}.supplier "
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

    tgt_qrc = QueryConfig(table_conf, tgt_schema, "target", "databricks")
    actual_tgt_query = HashQueryBuilder(tgt_qrc).build_query()
    expected_tgt_query = (
        "select sha2(concat(coalesce(trim(s_address_t),''), "
        "coalesce(trim(s_name),''), coalesce(trim(s_suppkey_t),'')),256) as "
        "hash_value__recon, coalesce(trim(s_suppkey_t),'') as s_suppkey from {catalog_name}.{schema_name}.supplier "
        "where  1 = 1 "
    )

    assert actual_tgt_query == expected_tgt_query


def test_hash_query_builder_with_transformations_with_drop_and_default_select():
    table_conf = Table(
        source_name="supplier",
        target_name="supplier",
        jdbc_reader_options=None,
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

    src_qrc = QueryConfig(table_conf, src_schema, "source", "oracle")
    actual_src_query = HashQueryBuilder(src_qrc).build_query()
    expected_src_query = (
        "select lower(RAWTOHEX(STANDARD_HASH(coalesce(trim(s_nationkey),'') || "
        "coalesce(trim(s_suppkey),'') || trim(s_address) || trim(s_name) || "
        "trim(s_phone) || trim(to_char(s_acctbal_t, '9999999999.99')), 'SHA256'))) as "
        "hash_value__recon, coalesce(trim(s_suppkey),'') as s_suppkey from {schema_name}.supplier "
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

    tgt_qrc = QueryConfig(table_conf, tgt_schema, "target", "databricks")
    actual_tgt_query = HashQueryBuilder(tgt_qrc).build_query()
    expected_tgt_query = (
        "select sha2(concat(cast(s_acctbal_t as decimal(38,2)), "
        "coalesce(trim(s_nationkey_t),''), coalesce(trim(s_suppkey_t),''), "
        'trim(s_address_t), trim(s_name), trim(s_phone_t)),256) as hash_value__recon, '
        "coalesce(trim(s_suppkey_t),'') as s_suppkey from {catalog_name}.{schema_name}.supplier where  1 = 1 "
    )

    assert actual_tgt_query == expected_tgt_query


def test_hash_query_builder_with_jdbc_reader_options():
    table_conf = Table(
        source_name="supplier",
        target_name="supplier",
        jdbc_reader_options=JdbcReaderOptions(
            number_partitions=100, partition_column="s_nationkey", lower_bound="0", upper_bound="100"
        ),
        join_columns=["s_suppkey"],
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

    src_qrc = QueryConfig(table_conf, src_schema, "source", "oracle")
    actual_src_query = HashQueryBuilder(src_qrc).build_query()
    expected_src_query = (
        "select lower(RAWTOHEX(STANDARD_HASH(coalesce(trim(s_address),'') || "
        "coalesce(trim(s_name),'') || coalesce(trim(s_suppkey),''), 'SHA256'))) as "
        "hash_value__recon, coalesce(trim(s_nationkey),'') as s_nationkey,coalesce(trim(s_suppkey),'') as s_suppkey "
        "from {schema_name}.supplier "
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

    tgt_qrc = QueryConfig(table_conf, tgt_schema, "target", "databricks")
    actual_tgt_query = HashQueryBuilder(tgt_qrc).build_query()
    expected_tgt_query = (
        "select sha2(concat(coalesce(trim(s_address_t),''), "
        "coalesce(trim(s_name),''), coalesce(trim(s_suppkey_t),'')),256) as "
        "hash_value__recon, coalesce(trim(s_suppkey_t),'') as s_suppkey from {catalog_name}.{schema_name}.supplier "
        "where  1 = 1 "
    )

    assert actual_tgt_query == expected_tgt_query


def test_hash_query_builder_with_threshold():
    table_conf = Table(
        source_name="supplier",
        target_name="supplier",
        jdbc_reader_options=JdbcReaderOptions(
            number_partitions=100, partition_column="s_nationkey", lower_bound="0", upper_bound="100"
        ),
        join_columns=["s_suppkey"],
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

    src_qrc = QueryConfig(table_conf, src_schema, "source", "oracle")
    actual_src_query = HashQueryBuilder(src_qrc).build_query()
    expected_src_query = (
        "select lower(RAWTOHEX(STANDARD_HASH(coalesce(trim(s_comment),'') || "
        "coalesce(trim(s_nationkey),'') || coalesce(trim(s_suppkey),'') || "
        "trim(s_address) || trim(s_name) || trim(s_phone), 'SHA256'))) as "
        "hash_value__recon, coalesce(trim(s_nationkey),'') as "
        "s_nationkey,coalesce(trim(s_suppkey),'') as s_suppkey from {schema_name}.supplier where  1 "
        '= 1 '
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

    tgt_qrc = QueryConfig(table_conf, tgt_schema, "target", "databricks")
    actual_tgt_query = HashQueryBuilder(tgt_qrc).build_query()
    expected_tgt_query = (
        "select sha2(concat(coalesce(trim(s_comment),''), "
        "coalesce(trim(s_nationkey),''), coalesce(trim(s_suppkey_t),''), "
        'trim(s_address_t), trim(s_name), trim(s_phone)),256) as hash_value__recon, '
        "coalesce(trim(s_suppkey_t),'') as s_suppkey from {catalog_name}.{schema_name}.supplier where  1 = 1 "
    )

    assert actual_tgt_query == expected_tgt_query


def test_hash_query_builder_with_filters():
    table_conf = Table(
        source_name="supplier",
        target_name="supplier",
        jdbc_reader_options=None,
        join_columns=["s_suppkey"],
        select_columns=["s_suppkey", "s_name", "s_address"],
        drop_columns=None,
        column_mapping=[
            ColumnMapping(source_name="s_suppkey", target_name="s_suppkey_t"),
            ColumnMapping(source_name="s_address", target_name="s_address_t"),
        ],
        transformations=None,
        thresholds=None,
        filters=Filters(source="s_name='t' and s_address='a'", target="s_name='t' and s_address_t='a'"),
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

    src_qrc = QueryConfig(table_conf, src_schema, "source", "snowflake")
    actual_src_query = HashQueryBuilder(src_qrc).build_query()
    expected_src_query = (
        "select sha2(concat(coalesce(trim(s_address),''), coalesce(trim(s_name),''), "
        "coalesce(trim(s_suppkey),'')),256) as hash_value__recon, "
        "coalesce(trim(s_suppkey),'') as s_suppkey from {catalog_name}.{schema_name}.supplier where s_name='t' and "
        "s_address='a'"
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

    tgt_qrc = QueryConfig(table_conf, tgt_schema, "target", "databricks")
    actual_tgt_query = HashQueryBuilder(tgt_qrc).build_query()
    expected_tgt_query = (
        "select sha2(concat(coalesce(trim(s_address_t),''), "
        "coalesce(trim(s_name),''), coalesce(trim(s_suppkey_t),'')),256) as "
        "hash_value__recon, coalesce(trim(s_suppkey_t),'') as s_suppkey from {catalog_name}.{schema_name}.supplier "
        "where s_name='t' and s_address_t='a'"
    )

    assert actual_tgt_query == expected_tgt_query


def test_hash_query_builder_with_unsupported_source():
    table_conf = Table(
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

    src_qrc = QueryConfig(table_conf, src_schema, "source", "abc")
    query_builder = HashQueryBuilder(src_qrc)

    with pytest.raises(Exception) as exc_info:
        query_builder.build_query()

    assert str(exc_info.value) == "Unsupported source type --> abc"


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
    src_schema = [
        Schema("s_suppkey", "number"),
        Schema("s_name", "varchar"),
        Schema("s_address", "varchar"),
        Schema("s_nationkey", "number"),
        Schema("s_phone", "varchar"),
        Schema("s_acctbal", "number"),
        Schema("s_comment", "varchar"),
    ]

    src_qrc = QueryConfig(table_conf, src_schema, "source", "oracle")
    actual_src_query = ThresholdQueryBuilder(src_qrc).build_query()
    expected_src_query = (
        'select s_acctbal as s_acctbal,s_suppkey as s_suppkey from {schema_name}.supplier where  1 = 1 '
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

    tgt_qrc = QueryConfig(table_conf, tgt_schema, "target", "databricks")
    actual_tgt_query = ThresholdQueryBuilder(tgt_qrc).build_query()
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
    src_schema = [
        Schema("s_suppkey", "number"),
        Schema("s_name", "varchar"),
        Schema("s_address", "varchar"),
        Schema("s_nationkey", "number"),
        Schema("s_phone", "varchar"),
        Schema("s_acctbal", "number"),
        Schema("s_comment", "varchar"),
        Schema("s_suppdate", "timestamp"),
    ]

    src_qrc = QueryConfig(table_conf, src_schema, "source", "oracle")
    actual_src_query = ThresholdQueryBuilder(src_qrc).build_query()
    expected_src_query = (
        "select trim(to_char(s_acctbal, '9999999999.99')) as s_acctbal,s_nationkey "
        "as s_nationkey,s_suppdate as s_suppdate,trim(s_suppkey) as s_suppkey from "
        "{schema_name}.supplier where  1 = 1 "
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
        Schema("s_suppdate_t", "timestamp"),
    ]

    tgt_qrc = QueryConfig(table_conf, tgt_schema, "target", "databricks")
    actual_tgt_query = ThresholdQueryBuilder(tgt_qrc).build_query()
    expected_tgt_query = (
        "select cast(s_acctbal_t as decimal(38,2)) as s_acctbal,s_suppdate_t as "
        "s_suppdate,trim(s_suppkey_t) as s_suppkey from {catalog_name}.{schema_name}.supplier where  1 = 1 "
    )

    assert actual_tgt_query == expected_tgt_query
