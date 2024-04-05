from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType

from databricks.labs.remorph.reconcile.query_builder.sampling_query import SamplingQueryBuilder
from databricks.labs.remorph.reconcile.recon_config import ColumnMapping, Table, Filters


def test_build_query_for_oracle_src(mock_spark_session, table_conf, source_schema, target_schema):
    spark = mock_spark_session
    schema = StructType([
        StructField('s_suppkey', IntegerType()),
        StructField('s_name', StringType()),
        StructField('s_address', StringType()),
        StructField('s_nationkey', IntegerType()),
        StructField('s_phone', StringType()),
        StructField('s_acctbal', StringType()),
        StructField('s_comment', StringType())
    ])
    df = spark.createDataFrame([
        (1, 'name-1', 'add-1', 11, '1-1', 100, 'c-1'),
        (2, 'name-2', 'add-2', 22, '2-2', 200, 'c-2'),
    ], schema=schema)

    conf = table_conf(join_columns=["s_suppkey", "s_nationkey"],
                      column_mapping=[ColumnMapping(source_name="s_suppkey", target_name="s_suppkey_t"),
                                      ColumnMapping(source_name="s_nationkey", target_name='s_nationkey_t'),
                                      ColumnMapping(source_name="s_address", target_name="s_address_t"),
                                      ColumnMapping(source_name="s_phone", target_name="s_phone_t"),
                                      ColumnMapping(source_name="s_acctbal", target_name="s_acctbal_t"),
                                      ColumnMapping(source_name="s_comment", target_name="s_comment_t"),
                                      ])

    src_actual = SamplingQueryBuilder(conf, source_schema, "source", "oracle").build_query(df)
    src_expected = ("with recon as (select '11' as s_nationkey, '1' as s_suppkey from dual "
                    'union \n'
                    "select '22' as s_nationkey, '2' as s_suppkey from dual), src as ( select "
                    "coalesce(trim(s_acctbal),'') as s_acctbal,coalesce(trim(s_address),'') as "
                    "s_address,coalesce(trim(s_comment),'') as "
                    "s_comment,coalesce(trim(s_name),'') as s_name,coalesce(trim(s_nationkey),'') "
                    "as s_nationkey,coalesce(trim(s_phone),'') as "
                    "s_phone,coalesce(trim(s_suppkey),'') as s_suppkey from "
                    '{schema_name}.supplier where  1 = 1  ) select src.* from src join recon on '
                    'recon.s_nationkey = src.s_nationkey and recon.s_suppkey = src.s_suppkey')

    tgt_actual = SamplingQueryBuilder(conf, target_schema, "target", "databricks").build_query(df)
    tgt_expected = ("with recon as (select '11' as s_nationkey, '1' as s_suppkey union \n"
                    "select '22' as s_nationkey, '2' as s_suppkey), src as ( select "
                    "coalesce(trim(s_acctbal_t),'') as s_acctbal,coalesce(trim(s_address_t),'') "
                    "as s_address,coalesce(trim(s_comment_t),'') as "
                    "s_comment,coalesce(trim(s_name),'') as "
                    "s_name,coalesce(trim(s_nationkey_t),'') as "
                    "s_nationkey,coalesce(trim(s_phone_t),'') as "
                    "s_phone,coalesce(trim(s_suppkey_t),'') as s_suppkey from "
                    '{catalog_name}.{schema_name}.target_supplier where  1 = 1  ) select src.* '
                    'from src join recon on recon.s_nationkey = src.s_nationkey and '
                    'recon.s_suppkey = src.s_suppkey')

    assert src_actual == src_expected
    assert tgt_actual == tgt_expected


def test_build_query_for_snowflake_src(mock_spark_session, table_conf, source_schema, target_schema):
    spark = mock_spark_session
    schema = StructType([
        StructField('s_suppkey', IntegerType()),
        StructField('s_name', StringType()),
        StructField('s_address', StringType()),
        StructField('s_nationkey', IntegerType()),
        StructField('s_phone', StringType()),
        StructField('s_acctbal', StringType()),
        StructField('s_comment', StringType())
    ])
    df = spark.createDataFrame([
        (1, 'name-1', 'add-1', 11, '1-1', 100, 'c-1'),
        (2, 'name-2', 'add-2', 22, '2-2', 200, 'c-2'),
    ], schema=schema)

    conf = table_conf(join_columns=["s_suppkey", "s_nationkey"],
                      column_mapping=[ColumnMapping(source_name="s_suppkey", target_name="s_suppkey_t"),
                                      ColumnMapping(source_name="s_nationkey", target_name='s_nationkey_t'),
                                      ColumnMapping(source_name="s_address", target_name="s_address_t"),
                                      ColumnMapping(source_name="s_phone", target_name="s_phone_t"),
                                      ColumnMapping(source_name="s_acctbal", target_name="s_acctbal_t"),
                                      ColumnMapping(source_name="s_comment", target_name="s_comment_t")],
                      filters=Filters(source="s_nationkey=1")
                      )

    src_actual = SamplingQueryBuilder(conf, source_schema, "source", "snowflake").build_query(df)
    src_expected = ("with recon as (select '11' as s_nationkey, '1' as s_suppkey union \n"
                    "select '22' as s_nationkey, '2' as s_suppkey), src as ( select "
                    "coalesce(trim(s_acctbal),'') as s_acctbal,coalesce(trim(s_address),'') as "
                    "s_address,coalesce(trim(s_comment),'') as "
                    "s_comment,coalesce(trim(s_name),'') as s_name,coalesce(trim(s_nationkey),'') "
                    "as s_nationkey,coalesce(trim(s_phone),'') as "
                    "s_phone,coalesce(trim(s_suppkey),'') as s_suppkey from "
                    '{catalog_name}.{schema_name}.supplier where s_nationkey=1 ) select src.* from src '
                    'join recon on recon.s_nationkey = src.s_nationkey and recon.s_suppkey = '
                    'src.s_suppkey')

    tgt_actual = SamplingQueryBuilder(conf, target_schema, "target", "databricks").build_query(df)
    tgt_expected = ("with recon as (select '11' as s_nationkey, '1' as s_suppkey union \n"
                    "select '22' as s_nationkey, '2' as s_suppkey), src as ( select "
                    "coalesce(trim(s_acctbal_t),'') as s_acctbal,coalesce(trim(s_address_t),'') "
                    "as s_address,coalesce(trim(s_comment_t),'') as "
                    "s_comment,coalesce(trim(s_name),'') as "
                    "s_name,coalesce(trim(s_nationkey_t),'') as "
                    "s_nationkey,coalesce(trim(s_phone_t),'') as "
                    "s_phone,coalesce(trim(s_suppkey_t),'') as s_suppkey from "
                    '{catalog_name}.{schema_name}.target_supplier where 1=1 ) select src.* '
                    'from src join recon on recon.s_nationkey = src.s_nationkey and '
                    'recon.s_suppkey = src.s_suppkey')

    assert src_actual == src_expected
    assert tgt_actual == tgt_expected
