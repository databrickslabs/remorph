from pyspark.sql.types import IntegerType, StringType, StructField, StructType

from databricks.labs.remorph.reconcile.dialects.utils import get_dialect
from databricks.labs.remorph.reconcile.query_builder.sampling_query import (
    SamplingQueryBuilder,
)
from databricks.labs.remorph.reconcile.recon_config import (
    ColumnMapping,
    Filters,
    ColumnType,
    Transformation,
    Layer,
)


def test_build_query_for_snowflake_src(mock_spark, table_mapping_builder, column_and_aliases_types):
    spark = mock_spark
    sch, sch_with_alias = column_and_aliases_types
    df_schema = StructType(
        [
            StructField('s_suppkey', IntegerType()),
            StructField('s_name', StringType()),
            StructField('s_address', StringType()),
            StructField('s_nationkey', IntegerType()),
            StructField('s_phone', StringType()),
            StructField('s_acctbal', StringType()),
            StructField('s_comment', StringType()),
        ]
    )
    df = spark.createDataFrame(
        [
            (1, 'name-1', 'add-1', 11, '1-1', 100, 'c-1'),
            (2, 'name-2', 'add-2', 22, '2-2', 200, 'c-2'),
        ],
        schema=df_schema,
    )

    conf = table_mapping_builder(
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
        transformations=[Transformation(column_name="s_address", source="trim(s_address)", target="trim(s_address_t)")],
    )

    src_actual = SamplingQueryBuilder(conf, sch, Layer.SOURCE, get_dialect("snowflake")).build_query(df)

    src_expected = (
        "WITH recon AS (SELECT CAST(11 AS number) AS s_nationkey, CAST(1 AS number) "
        "AS s_suppkey UNION SELECT CAST(22 AS number) AS s_nationkey, CAST(2 AS "
        "number) AS s_suppkey), src AS (SELECT COALESCE(TRIM(s_acctbal), '_null_recon_') "
        "AS s_acctbal, TRIM(s_address) AS s_address, COALESCE(TRIM(s_comment), '_null_recon_') AS "
        "s_comment, COALESCE(TRIM(s_name), '_null_recon_') AS s_name, COALESCE(TRIM(s_nationkey), "
        "'_null_recon_') AS s_nationkey, COALESCE(TRIM(s_phone), '_null_recon_') AS s_phone, "
        "COALESCE(TRIM(s_suppkey), '_null_recon_') AS s_suppkey FROM :tbl WHERE s_nationkey = 1) "
        'SELECT src.s_acctbal, src.s_address, src.s_comment, src.s_name, src.s_nationkey, src.s_phone, '
        "src.s_suppkey FROM src INNER JOIN recon AS recon ON "
        "src.s_nationkey = recon.s_nationkey AND src.s_suppkey = recon.s_suppkey"
    )

    tgt_actual = SamplingQueryBuilder(conf, sch_with_alias, Layer.TARGET, get_dialect("databricks")).build_query(df)

    tgt_expected = (
        'WITH recon AS (SELECT 11 AS s_nationkey, 1 AS s_suppkey UNION SELECT 22 AS '
        "s_nationkey, 2 AS s_suppkey), src AS (SELECT COALESCE(TRIM(s_acctbal_t), '_null_recon_') "
        'AS s_acctbal, TRIM(s_address_t) AS s_address, COALESCE(TRIM(s_comment_t), '
        "'_null_recon_') AS s_comment, COALESCE(TRIM(s_name), '_null_recon_') AS s_name, "
        "COALESCE(TRIM(s_nationkey_t), '_null_recon_') AS s_nationkey, COALESCE(TRIM(s_phone_t), "
        "'_null_recon_') AS s_phone, COALESCE(TRIM(s_suppkey_t), '_null_recon_') AS s_suppkey FROM :tbl) "
        'SELECT src.s_acctbal, src.s_address, src.s_comment, src.s_name, src.s_nationkey, src.s_phone, '
        "src.s_suppkey FROM src INNER JOIN recon AS recon ON src.s_nationkey = recon.s_nationkey "
        "AND src.s_suppkey = recon.s_suppkey"
    )

    assert src_expected == src_actual
    assert tgt_expected == tgt_actual


def test_build_query_for_oracle_src(mock_spark, table_mapping_builder, column_and_aliases_types, column_mappings):
    spark = mock_spark
    _, sch_with_alias = column_and_aliases_types
    df_schema = StructType(
        [
            StructField('s_suppkey', IntegerType()),
            StructField('s_name', StringType()),
            StructField('s_address', StringType()),
            StructField('s_nationkey', IntegerType()),
            StructField('s_phone', StringType()),
            StructField('s_acctbal', StringType()),
            StructField('s_comment', StringType()),
        ]
    )
    df = spark.createDataFrame(
        [
            (1, 'name-1', 'add-1', 11, '1-1', 100, 'c-1'),
            (2, 'name-2', 'add-2', 22, '2-2', 200, 'c-2'),
            (3, 'name-3', 'add-3', 33, '3-3', 300, 'c-3'),
        ],
        schema=df_schema,
    )

    conf = table_mapping_builder(
        join_columns=["s_suppkey", "s_nationkey"],
        column_mapping=column_mappings,
        filters=Filters(source="s_nationkey=1"),
    )

    sch = [
        ColumnType("s_suppkey", "number"),
        ColumnType("s_name", "varchar"),
        ColumnType("s_address", "varchar"),
        ColumnType("s_nationkey", "number"),
        ColumnType("s_phone", "nvarchar"),
        ColumnType("s_acctbal", "number"),
        ColumnType("s_comment", "nchar"),
    ]

    src_actual = SamplingQueryBuilder(conf, sch, Layer.SOURCE, get_dialect("oracle")).build_query(df)
    src_expected = (
        'WITH recon AS (SELECT CAST(11 AS number) AS s_nationkey, CAST(1 AS number) '
        'AS s_suppkey FROM dual UNION SELECT CAST(22 AS number) AS s_nationkey, '
        'CAST(2 AS number) AS s_suppkey FROM dual UNION SELECT CAST(33 AS number) AS '
        's_nationkey, CAST(3 AS number) AS s_suppkey FROM dual), '
        "src AS (SELECT COALESCE(TRIM(s_acctbal), '_null_recon_') AS s_acctbal, "
        "COALESCE(TRIM(s_address), '_null_recon_') AS s_address, "
        "NVL(TRIM(TO_CHAR(s_comment)),'_null_recon_') AS s_comment, "
        "COALESCE(TRIM(s_name), '_null_recon_') AS s_name, COALESCE(TRIM(s_nationkey), '_null_recon_') AS "
        "s_nationkey, NVL(TRIM(TO_CHAR(s_phone)),'_null_recon_') AS s_phone, "
        "COALESCE(TRIM(s_suppkey), '_null_recon_') AS s_suppkey FROM :tbl WHERE s_nationkey = 1) "
        'SELECT src.s_acctbal, src.s_address, src.s_comment, src.s_name, src.s_nationkey, src.s_phone, '
        "src.s_suppkey FROM src INNER JOIN recon recon ON "
        "src.s_nationkey = recon.s_nationkey AND src.s_suppkey = recon.s_suppkey"
    )

    tgt_actual = SamplingQueryBuilder(conf, sch_with_alias, Layer.TARGET, get_dialect("databricks")).build_query(df)
    tgt_expected = (
        'WITH recon AS (SELECT 11 AS s_nationkey, 1 AS s_suppkey UNION SELECT 22 AS '
        's_nationkey, 2 AS s_suppkey UNION SELECT 33 AS s_nationkey, 3 AS s_suppkey), '
        "src AS (SELECT COALESCE(TRIM(s_acctbal_t), '_null_recon_') AS s_acctbal, "
        "COALESCE(TRIM(s_address_t), '_null_recon_') AS s_address, COALESCE(TRIM(s_comment_t), "
        "'_null_recon_') AS s_comment, COALESCE(TRIM(s_name), '_null_recon_') AS s_name, "
        "COALESCE(TRIM(s_nationkey_t), '_null_recon_') AS s_nationkey, COALESCE(TRIM(s_phone_t), "
        "'_null_recon_') AS s_phone, COALESCE(TRIM(s_suppkey_t), '_null_recon_') AS s_suppkey FROM :tbl) "
        'SELECT src.s_acctbal, src.s_address, src.s_comment, src.s_name, src.s_nationkey, src.s_phone, '
        "src.s_suppkey FROM src INNER JOIN recon AS recon ON "
        "src.s_nationkey = recon.s_nationkey AND src.s_suppkey = recon.s_suppkey"
    )

    assert src_expected == src_actual
    assert tgt_expected == tgt_actual


def test_build_query_for_databricks_src(mock_spark, table_mapping_builder):
    spark = mock_spark
    df_schema = StructType(
        [
            StructField('s_suppkey', IntegerType()),
            StructField('s_name', StringType()),
            StructField('s_address', StringType()),
            StructField('s_nationkey', IntegerType()),
            StructField('s_phone', StringType()),
            StructField('s_acctbal', StringType()),
            StructField('s_comment', StringType()),
        ]
    )
    df = spark.createDataFrame([(1, 'name-1', 'add-1', 11, '1-1', 100, 'c-1')], schema=df_schema)

    schema = [
        ColumnType("s_suppkey", "bigint"),
        ColumnType("s_name", "string"),
        ColumnType("s_address", "string"),
        ColumnType("s_nationkey", "bigint"),
        ColumnType("s_phone", "string"),
        ColumnType("s_acctbal", "bigint"),
        ColumnType("s_comment", "string"),
    ]

    conf = table_mapping_builder(join_columns=["s_suppkey", "s_nationkey"])

    src_actual = SamplingQueryBuilder(conf, schema, Layer.SOURCE, get_dialect("databricks")).build_query(df)
    src_expected = (
        'WITH recon AS (SELECT CAST(11 AS bigint) AS s_nationkey, CAST(1 AS bigint) AS s_suppkey), src AS (SELECT '
        "COALESCE(TRIM(s_acctbal), '_null_recon_') AS s_acctbal, COALESCE(TRIM(s_address), '_null_recon_') AS "
        "s_address, COALESCE(TRIM(s_comment), '_null_recon_') AS s_comment, "
        "COALESCE(TRIM(s_name), '_null_recon_') AS s_name, COALESCE(TRIM(s_nationkey), '_null_recon_') AS "
        "s_nationkey, COALESCE(TRIM(s_phone), '_null_recon_') AS s_phone, "
        "COALESCE(TRIM(s_suppkey), '_null_recon_') AS s_suppkey FROM :tbl) SELECT src.s_acctbal, "
        'src.s_address, src.s_comment, src.s_name, src.s_nationkey, src.s_phone, src.s_suppkey FROM src INNER '
        "JOIN recon AS recon ON src.s_nationkey = recon.s_nationkey AND src.s_suppkey = recon.s_suppkey"
    )
    assert src_expected == src_actual


def test_build_query_for_snowflake_without_transformations(mock_spark, table_mapping_builder, column_and_aliases_types):
    spark = mock_spark
    sch, sch_with_alias = column_and_aliases_types
    df_schema = StructType(
        [
            StructField('s_suppkey', IntegerType()),
            StructField('s_name', StringType()),
            StructField('s_address', StringType()),
            StructField('s_nationkey', IntegerType()),
            StructField('s_phone', StringType()),
            StructField('s_acctbal', StringType()),
            StructField('s_comment', StringType()),
        ]
    )
    df = spark.createDataFrame(
        [
            (1, 'name-1', 'add-1', 11, '1-1', 100, 'c-1'),
            (2, 'name-2', 'add-2', 22, '2-2', 200, 'c-2'),
        ],
        schema=df_schema,
    )

    conf = table_mapping_builder(
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
        transformations=[
            Transformation(column_name="s_address", source=None, target="trim(s_address_t)"),
            Transformation(column_name="s_name", source="trim(s_name)", target=None),
            Transformation(column_name="s_suppkey", source="trim(s_suppkey)", target=None),
        ],
    )

    src_actual = SamplingQueryBuilder(conf, sch, Layer.SOURCE, get_dialect("snowflake")).build_query(df)
    src_expected = (
        'WITH recon AS (SELECT CAST(11 AS number) AS s_nationkey, 1 AS s_suppkey '
        'UNION SELECT CAST(22 AS number) AS s_nationkey, 2 AS s_suppkey), src '
        "AS (SELECT COALESCE(TRIM(s_acctbal), '_null_recon_') "
        "AS s_acctbal, s_address AS s_address, COALESCE(TRIM(s_comment), '_null_recon_') AS "
        "s_comment, TRIM(s_name) AS s_name, COALESCE(TRIM(s_nationkey), "
        "'_null_recon_') AS s_nationkey, COALESCE(TRIM(s_phone), '_null_recon_') AS s_phone, "
        "TRIM(s_suppkey) AS s_suppkey FROM :tbl WHERE s_nationkey = 1) "
        'SELECT src.s_acctbal, src.s_address, src.s_comment, src.s_name, src.s_nationkey, src.s_phone, '
        "src.s_suppkey FROM src INNER JOIN recon AS recon ON "
        "src.s_nationkey = recon.s_nationkey AND src.s_suppkey = recon.s_suppkey"
    )

    tgt_actual = SamplingQueryBuilder(conf, sch_with_alias, Layer.TARGET, get_dialect("databricks")).build_query(df)
    tgt_expected = (
        'WITH recon AS (SELECT 11 AS s_nationkey, 1 AS s_suppkey UNION SELECT 22 AS '
        "s_nationkey, 2 AS s_suppkey), src AS (SELECT COALESCE(TRIM(s_acctbal_t), '_null_recon_') "
        'AS s_acctbal, TRIM(s_address_t) AS s_address, COALESCE(TRIM(s_comment_t), '
        "'_null_recon_') AS s_comment, s_name AS s_name, "
        "COALESCE(TRIM(s_nationkey_t), '_null_recon_') AS s_nationkey, COALESCE(TRIM(s_phone_t), "
        "'_null_recon_') AS s_phone, s_suppkey_t AS s_suppkey FROM :tbl) "
        'SELECT src.s_acctbal, src.s_address, src.s_comment, src.s_name, src.s_nationkey, src.s_phone, '
        "src.s_suppkey FROM src INNER JOIN recon AS recon ON "
        "src.s_nationkey = recon.s_nationkey AND src.s_suppkey = recon.s_suppkey"
    )

    assert src_expected == src_actual
    assert tgt_expected == tgt_actual


def test_build_query_for_snowflake_src_for_non_integer_primary_keys(mock_spark, table_mapping_builder):
    spark = mock_spark
    sch = [ColumnType("s_suppkey", "varchar"), ColumnType("s_name", "varchar"), ColumnType("s_nationkey", "number")]

    sch_with_alias = [
        ColumnType("s_suppkey_t", "varchar"),
        ColumnType("s_name", "varchar"),
        ColumnType("s_nationkey_t", "number"),
    ]
    df_schema = StructType(
        [
            StructField('s_suppkey', StringType()),
            StructField('s_name', StringType()),
            StructField('s_nationkey', IntegerType()),
        ]
    )
    df = spark.createDataFrame(
        [
            ('a', 'name-1', 11),
            ('b', 'name-2', 22),
        ],
        schema=df_schema,
    )

    conf = table_mapping_builder(
        join_columns=["s_suppkey", "s_nationkey"],
        column_mapping=[
            ColumnMapping(source_name="s_suppkey", target_name="s_suppkey_t"),
            ColumnMapping(source_name="s_nationkey", target_name='s_nationkey_t'),
        ],
        transformations=[Transformation(column_name="s_address", source="trim(s_address)", target="trim(s_address_t)")],
    )

    src_actual = SamplingQueryBuilder(conf, sch, Layer.SOURCE, get_dialect("snowflake")).build_query(df)
    src_expected = (
        "WITH recon AS (SELECT CAST(11 AS number) AS s_nationkey, CAST('a' AS "
        'varchar) AS s_suppkey UNION SELECT CAST(22 AS number) AS s_nationkey, '
        "CAST('b' AS varchar) AS s_suppkey), src AS (SELECT COALESCE(TRIM(s_name), '_null_recon_') AS s_name, "
        "COALESCE(TRIM("
        "s_nationkey), '_null_recon_') AS s_nationkey, COALESCE(TRIM(s_suppkey), '_null_recon_') AS s_suppkey FROM "
        ":tbl) "
        "SELECT src.s_name, src.s_nationkey, src.s_suppkey FROM src INNER JOIN recon AS recon ON "
        "src.s_nationkey = recon.s_nationkey AND src.s_suppkey = recon.s_suppkey"
    )

    tgt_actual = SamplingQueryBuilder(conf, sch_with_alias, Layer.TARGET, get_dialect("databricks")).build_query(df)
    tgt_expected = (
        "WITH recon AS (SELECT 11 AS s_nationkey, 'a' AS s_suppkey UNION SELECT 22 AS "
        "s_nationkey, 'b' AS s_suppkey), src AS (SELECT COALESCE(TRIM(s_name), '_null_recon_') AS s_name, "
        "COALESCE(TRIM(s_nationkey_t), '_null_recon_') AS s_nationkey, COALESCE(TRIM(s_suppkey_t), '_null_recon_') AS "
        "s_suppkey FROM :tbl) "
        "SELECT src.s_name, src.s_nationkey, "
        "src.s_suppkey FROM src INNER JOIN recon AS recon ON "
        "src.s_nationkey = recon.s_nationkey AND src.s_suppkey = recon.s_suppkey"
    )

    assert src_expected == src_actual
    assert tgt_expected == tgt_actual
