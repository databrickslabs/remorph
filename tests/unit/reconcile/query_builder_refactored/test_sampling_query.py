from pyspark.sql.types import IntegerType, StringType, StructField, StructType

from databricks.labs.remorph.reconcile.query_builder_refactored.recon_config import (
    ColumnMapping,
    Filters,
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
    )

    src_actual = SamplingQueryBuilder(conf, sch, "source", "snowflake").build_query(df)
    print(src_actual)
