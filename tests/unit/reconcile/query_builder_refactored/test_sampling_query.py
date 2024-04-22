from pyspark.sql.types import IntegerType, StringType, StructField, StructType

from databricks.labs.remorph.reconcile.query_builder_refactored.recon_config import (
    ColumnMapping,
    Filters,
    Transformation,
)
from databricks.labs.remorph.reconcile.query_builder_refactored.sampling_query import (
    SamplingQueryBuilder,
)


def test_build_query_for_snowflake_src(mock_spark_session, table_conf_mock, schema):
    spark = mock_spark_session
    sch, sch_with_alias = schema
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

    src_actual = SamplingQueryBuilder(conf, sch, "source", "snowflake").build_query(df)
    src_expected = (
        "WITH recon AS (SELECT 11 AS s_nationkey, 1 AS s_suppkey UNION SELECT 22 AS s_nationkey, "
        "2 AS s_suppkey), src AS (SELECT COALESCE(TRIM(s_acctbal), '') AS s_acctbal, TRIM(s_address) AS "
        "s_address, COALESCE(TRIM(s_comment), '') AS s_comment, COALESCE(TRIM(s_name), '') AS s_name, "
        "COALESCE(TRIM(s_nationkey), '') AS s_nationkey, COALESCE(TRIM(s_phone), '') AS s_phone, "
        "COALESCE(TRIM(s_suppkey), '') AS s_suppkey FROM :tbl WHERE s_nationkey = 1) SELECT src.* FROM "
        "src INNER JOIN recon USING (s_nationkey, s_suppkey)"
    )

    tgt_actual = SamplingQueryBuilder(conf, sch_with_alias, "target", "databricks").build_query(df)
    tgt_expected = (
        "WITH recon AS (SELECT 11 AS s_nationkey, 1 AS s_suppkey UNION SELECT 22 AS s_nationkey, "
        "2 AS s_suppkey), src AS (SELECT COALESCE(TRIM(s_acctbal_t), '') AS s_acctbal, TRIM(s_address_t) "
        "AS s_address, COALESCE(TRIM(s_comment_t), '') AS s_comment, COALESCE(TRIM(s_name), "
        "'') AS s_name, COALESCE(TRIM(s_nationkey_t), '') AS s_nationkey, COALESCE(TRIM(s_phone_t), "
        "'') AS s_phone, COALESCE(TRIM(s_suppkey_t), '') AS s_suppkey FROM :tbl) SELECT src.* FROM src "
        "INNER JOIN recon USING (s_nationkey, s_suppkey)"
    )

    assert src_expected == src_actual
    assert tgt_expected == tgt_actual
