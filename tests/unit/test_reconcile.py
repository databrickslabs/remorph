from databricks.labs.remorph.reconcile.execute import (
    build_query,
    generate_transformation_rule_mapping,
)
from databricks.labs.remorph.reconcile.recon_config import (
    ColumnMapping,
    JdbcReaderOptions,
    JoinColumns,
    Schema,
    Tables,
    Transformation,
)


def test_build_query_src():
    table_conf = Tables(
        source_name="supplier",
        target_name="supplier",
        jdbc_reader_options=JdbcReaderOptions(
            number_partitions=10, partition_column="s_suppkey", lower_bound="0", upper_bound="10000000", fetch_size=100
        ),
        join_columns=[JoinColumns(source_name="s_suppkey", target_name=None)],
        select_columns=None,
        drop_columns=None,
        column_mapping=[ColumnMapping(source_name="s_address", target_name="s_address_alias")],
        transformations=[
            Transformation(column_name="s_address", source="trim(s_address)", target="trim(s_address)"),
            Transformation(column_name="s_comment", source="trim(s_comment)", target="trim(s_comment)"),
            Transformation(column_name="s_name", source="trim(s_name)", target="trim(s_name)"),
            Transformation(
                column_name="s_acctbal",
                source="trim(to_char(s_acctbal, '9999999999.99'))",
                target="cast(s_acctbal as decimal(38,2))",
            ),
        ],
        thresholds=[],
        filters=None,
    )
    schema = [
        Schema("s_suppkey", "number"),
        Schema("s_name", "varchar"),
        Schema("s_address", "varchar"),
        Schema("s_nationkey", "number"),
        Schema("s_phone", "varchar"),
        Schema("s_acctbal", "number"),
        Schema("s_comment", "varchar"),
        Schema("s_creation_date", "date"),
    ]

    actual = build_query(table_conf=table_conf, schema=schema, layer="source", source="oracle")
    print(actual)


def test_build_query_tgt():
    table_conf = Tables(
        source_name="supplier",
        target_name="supplier",
        jdbc_reader_options=JdbcReaderOptions(
            number_partitions=10,
            partition_column="s_suppkey_alias",
            lower_bound="0",
            upper_bound="10000000",
            fetch_size=100,
        ),
        join_columns=[JoinColumns(source_name="s_suppkey", target_name="s_suppkey_alias")],
        select_columns=None,
        drop_columns=None,
        column_mapping=[ColumnMapping(source_name="s_suppkey", target_name="s_suppkey_alias")],
        transformations=[
            Transformation(column_name="s_address", source="trim(s_address)", target="trim(s_address)"),
            Transformation(column_name="s_comment", source="trim(s_comment)", target="trim(s_comment)"),
            Transformation(column_name="s_name", source="trim(s_name)", target="trim(s_name)"),
            Transformation(
                column_name="s_acctbal",
                source="trim(to_char(s_acctbal, '9999999999.99'))",
                target="cast(s_acctbal as decimal(38,2))",
            ),
        ],
        thresholds=[],
        filters=None,
    )
    schema = [
        Schema("s_suppkey_alias", "number"),
        Schema("s_name", "varchar"),
        Schema("s_address", "varchar"),
        Schema("s_nationkey", "number"),
        Schema("s_phone", "varchar"),
        Schema("s_acctbal", "number"),
        Schema("s_comment", "varchar"),
        Schema("s_creation_date", "date"),
    ]

    actual = build_query(table_conf=table_conf, schema=schema, layer="target", source="databricks")
    print(actual)


def test_generate_transformation_rule_mapping():
    table_conf = Tables(
        source_name="supplier",
        target_name="supplier",
        jdbc_reader_options=JdbcReaderOptions(
            number_partitions=10, partition_column="s_suppkey", lower_bound="0", upper_bound="10000000", fetch_size=100
        ),
        join_columns=[JoinColumns(source_name="s_suppkey", target_name=None)],
        select_columns=None,
        drop_columns=None,
        column_mapping=[ColumnMapping(source_name="s_address", target_name="s_address")],
        transformations=[
            Transformation(column_name="s_address", source="trim(s_address)", target="trim(s_address)"),
            Transformation(column_name="s_comment", source="trim(s_comment)", target="trim(s_comment)"),
            Transformation(column_name="s_name", source="trim(s_name)", target="trim(s_name)"),
            Transformation(
                column_name="s_acctbal",
                source="trim(to_char(s_acctbal, '9999999999.99'))",
                target="cast(s_acctbal as decimal(38,2))",
            ),
        ],
        thresholds=[],
        filters=None,
    )
    schema = [
        Schema("s_suppkey", "number"),
        Schema("s_name", "varchar"),
        Schema("s_address", "varchar"),
        Schema("s_nationkey", "number"),
        Schema("s_phone", "varchar"),
        Schema("s_acctbal", "number"),
        Schema("s_comment", "varchar"),
        Schema("s_creation_date", "date"),
    ]

    final_columns = [
        "s_suppkey",
        "s_name",
        "s_address",
        "s_nationkey",
        "s_phone",
        "s_acctbal",
        "s_comment",
        "s_creation_date",
    ]
    schema_info = {getattr(v, "column_name"): v for v in schema}
    generate_transformation_rule_mapping(final_columns, schema_info, table_conf, "oracle", "source")
