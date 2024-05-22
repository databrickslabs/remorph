from pyspark.sql.types import IntegerType, StringType, StructField, StructType

from databricks.labs.remorph.config import get_dialect
from databricks.labs.remorph.reconcile.query_builder.sampling_query import (
    SamplingQueryBuilder,
)
from databricks.labs.remorph.reconcile.recon_config import (
    ColumnMapping,
    Filters,
    Schema,
    Transformation,
)


def test_build_query_for_snowflake_src(mock_spark, table_conf_mock, table_schema):
    spark = mock_spark
    sch, sch_with_alias = table_schema
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

    conf = table_conf_mock(
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

    src_actual = SamplingQueryBuilder(conf, sch, "source", get_dialect("snowflake")).build_query(df)
    src_expected = (
        'WITH recon AS (SELECT 11 AS s_nationkey, 1 AS s_suppkey UNION SELECT 22 AS '
        "s_nationkey, 2 AS s_suppkey), src AS (SELECT COALESCE(TRIM(s_acctbal), '') "
        "AS s_acctbal, TRIM(s_address) AS s_address, COALESCE(TRIM(s_comment), '') AS "
        "s_comment, COALESCE(TRIM(s_name), '') AS s_name, COALESCE(TRIM(s_nationkey), "
        "'') AS s_nationkey, COALESCE(TRIM(s_phone), '') AS s_phone, "
        "COALESCE(TRIM(s_suppkey), '') AS s_suppkey FROM :tbl WHERE s_nationkey = 1) "
        'SELECT s_acctbal, s_address, s_comment, s_name, s_nationkey, s_phone, '
        's_suppkey FROM src INNER JOIN recon USING (s_nationkey, s_suppkey)'
    )

    tgt_actual = SamplingQueryBuilder(conf, sch_with_alias, "target", get_dialect("databricks")).build_query(df)
    tgt_expected = (
        'WITH recon AS (SELECT 11 AS s_nationkey, 1 AS s_suppkey UNION SELECT 22 AS '
        "s_nationkey, 2 AS s_suppkey), src AS (SELECT COALESCE(TRIM(s_acctbal_t), '') "
        'AS s_acctbal, TRIM(s_address_t) AS s_address, COALESCE(TRIM(s_comment_t), '
        "'') AS s_comment, COALESCE(TRIM(s_name), '') AS s_name, "
        "COALESCE(TRIM(s_nationkey_t), '') AS s_nationkey, COALESCE(TRIM(s_phone_t), "
        "'') AS s_phone, COALESCE(TRIM(s_suppkey_t), '') AS s_suppkey FROM :tbl) "
        'SELECT s_acctbal, s_address, s_comment, s_name, s_nationkey, s_phone, '
        's_suppkey FROM src INNER JOIN recon USING (s_nationkey, s_suppkey)'
    )

    assert src_expected == src_actual
    assert tgt_expected == tgt_actual


def test_build_query_for_oracle_src(mock_spark, table_conf_mock, table_schema, column_mapping):
    spark = mock_spark
    _, sch_with_alias = table_schema
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

    conf = table_conf_mock(
        join_columns=["s_suppkey", "s_nationkey"],
        column_mapping=column_mapping,
        filters=Filters(source="s_nationkey=1"),
    )

    sch = [
        Schema("s_suppkey", "number"),
        Schema("s_name", "varchar"),
        Schema("s_address", "varchar"),
        Schema("s_nationkey", "number"),
        Schema("s_phone", "nvarchar"),
        Schema("s_acctbal", "number"),
        Schema("s_comment", "nchar"),
    ]

    src_actual = SamplingQueryBuilder(conf, sch, "source", get_dialect("oracle")).build_query(df)
    src_expected = (
        'WITH recon AS (SELECT 11 AS s_nationkey, 1 AS s_suppkey UNION SELECT 22 AS '
        's_nationkey, 2 AS s_suppkey UNION SELECT 33 AS s_nationkey, 3 AS s_suppkey), '
        "src AS (SELECT COALESCE(TRIM(s_acctbal), '') AS s_acctbal, "
        "COALESCE(TRIM(s_address), '') AS s_address, "
        "NVL(TRIM(TO_CHAR(s_comment)),'_null_recon_') AS s_comment, "
        "COALESCE(TRIM(s_name), '') AS s_name, COALESCE(TRIM(s_nationkey), '') AS "
        "s_nationkey, NVL(TRIM(TO_CHAR(s_phone)),'_null_recon_') AS s_phone, "
        "COALESCE(TRIM(s_suppkey), '') AS s_suppkey FROM :tbl WHERE s_nationkey = 1) "
        'SELECT s_acctbal, s_address, s_comment, s_name, s_nationkey, s_phone, '
        's_suppkey FROM src INNER JOIN recon USING (s_nationkey, s_suppkey)'
    )

    tgt_actual = SamplingQueryBuilder(conf, sch_with_alias, "target", get_dialect("databricks")).build_query(df)
    tgt_expected = (
        'WITH recon AS (SELECT 11 AS s_nationkey, 1 AS s_suppkey UNION SELECT 22 AS '
        's_nationkey, 2 AS s_suppkey UNION SELECT 33 AS s_nationkey, 3 AS s_suppkey), '
        "src AS (SELECT COALESCE(TRIM(s_acctbal_t), '') AS s_acctbal, "
        "COALESCE(TRIM(s_address_t), '') AS s_address, COALESCE(TRIM(s_comment_t), "
        "'') AS s_comment, COALESCE(TRIM(s_name), '') AS s_name, "
        "COALESCE(TRIM(s_nationkey_t), '') AS s_nationkey, COALESCE(TRIM(s_phone_t), "
        "'') AS s_phone, COALESCE(TRIM(s_suppkey_t), '') AS s_suppkey FROM :tbl) "
        'SELECT s_acctbal, s_address, s_comment, s_name, s_nationkey, s_phone, '
        's_suppkey FROM src INNER JOIN recon USING (s_nationkey, s_suppkey)'
    )

    assert src_expected == src_actual
    assert tgt_expected == tgt_actual


def test_build_query_for_databricks_src(mock_spark, table_conf_mock):
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
        Schema("s_suppkey", "bigint"),
        Schema("s_name", "string"),
        Schema("s_address", "string"),
        Schema("s_nationkey", "bigint"),
        Schema("s_phone", "string"),
        Schema("s_acctbal", "bigint"),
        Schema("s_comment", "string"),
    ]

    conf = table_conf_mock(join_columns=["s_suppkey", "s_nationkey"])

    src_actual = SamplingQueryBuilder(conf, schema, "source", get_dialect("databricks")).build_query(df)
    src_expected = (
        'WITH recon AS (SELECT 11 AS s_nationkey, 1 AS s_suppkey), src AS (SELECT '
        "COALESCE(TRIM(s_acctbal), '') AS s_acctbal, COALESCE(TRIM(s_address), '') AS "
        "s_address, COALESCE(TRIM(s_comment), '') AS s_comment, "
        "COALESCE(TRIM(s_name), '') AS s_name, COALESCE(TRIM(s_nationkey), '') AS "
        "s_nationkey, COALESCE(TRIM(s_phone), '') AS s_phone, "
        "COALESCE(TRIM(s_suppkey), '') AS s_suppkey FROM :tbl) SELECT s_acctbal, "
        's_address, s_comment, s_name, s_nationkey, s_phone, s_suppkey FROM src INNER '
        'JOIN recon USING (s_nationkey, s_suppkey)'
    )
    assert src_expected == src_actual
