import pytest
from pyspark.sql import SparkSession
from sqlglot import parse_one

from databricks.labs.remorph.reconcile.recon_config import (
    ColumnMapping,
    Filters,
    JdbcReaderOptions,
    Schema,
    Table,
    Thresholds,
    Transformation,
)


@pytest.fixture
def mock_spark_session() -> SparkSession:
    """
    Method helps to create spark session
    :return: returns the spark session
    """
    return (
        SparkSession.builder.master("local[*]").appName("Remorph Reconcile Test").remote("sc://localhost").getOrCreate()
    )


@pytest.fixture
def table_conf_mock():
    def _mock_table_conf(**kwargs):
        return Table(
            source_name="supplier",
            target_name="supplier",
            jdbc_reader_options=kwargs.get('jdbc_reader_options', None),
            join_columns=kwargs.get('join_columns', None),
            select_columns=kwargs.get('select_columns', None),
            drop_columns=kwargs.get('drop_columns', None),
            column_mapping=kwargs.get('column_mapping', None),
            transformations=kwargs.get('transformations', None),
            thresholds=kwargs.get('thresholds', None),
            filters=kwargs.get('filters', None),
        )

    return _mock_table_conf


@pytest.fixture
def table_conf_with_opts(column_mapping):
    return Table(
        source_name="supplier",
        target_name="target_supplier",
        jdbc_reader_options=JdbcReaderOptions(
            number_partitions=100, partition_column="s_nationkey", lower_bound="0", upper_bound="100"
        ),
        join_columns=["s_suppkey", "s_nationkey"],
        select_columns=["s_suppkey", "s_name", "s_address", "s_phone", "s_acctbal", "s_nationkey"],
        drop_columns=["s_comment"],
        column_mapping=column_mapping,
        transformations=[
            Transformation(column_name="s_address", source="trim(s_address)", target="trim(s_address_t)"),
            Transformation(column_name="s_phone", source="trim(s_phone)", target="trim(s_phone_t)"),
            Transformation(column_name="s_name", source="trim(s_name)", target="trim(s_name)"),
        ],
        thresholds=[Thresholds(column_name="s_acctbal", lower_bound="0", upper_bound="100", type="int")],
        filters=Filters(source="s_name='t' and s_address='a'", target="s_name='t' and s_address_t='a'"),
    )


@pytest.fixture
def column_mapping():
    return [
        ColumnMapping(source_name="s_suppkey", target_name="s_suppkey_t"),
        ColumnMapping(source_name="s_address", target_name="s_address_t"),
        ColumnMapping(source_name="s_nationkey", target_name="s_nationkey_t"),
        ColumnMapping(source_name="s_phone", target_name="s_phone_t"),
        ColumnMapping(source_name="s_acctbal", target_name="s_acctbal_t"),
        ColumnMapping(source_name="s_comment", target_name="s_comment_t"),
    ]


@pytest.fixture
def schema():
    sch = [
        Schema("s_suppkey", "number"),
        Schema("s_name", "varchar"),
        Schema("s_address", "varchar"),
        Schema("s_nationkey", "number"),
        Schema("s_phone", "varchar"),
        Schema("s_acctbal", "number"),
        Schema("s_comment", "varchar"),
    ]

    sch_with_alias = [
        Schema("s_suppkey_t", "number"),
        Schema("s_name", "varchar"),
        Schema("s_address_t", "varchar"),
        Schema("s_nationkey_t", "number"),
        Schema("s_phone_t", "varchar"),
        Schema("s_acctbal_t", "number"),
        Schema("s_comment_t", "varchar"),
    ]

    return sch, sch_with_alias


@pytest.fixture
def expr():
    return parse_one("SELECT col1 FROM DUAL")


@pytest.fixture
def snowflake_databricks_schema():
    src_schema = [
        Schema("col_boolean", "boolean"),
        Schema("col_char", "varchar(1)"),
        Schema("col_varchar", "varchar(16777216)"),
        Schema("col_string", "varchar(16777216)"),
        Schema("col_text", "varchar(16777216)"),
        Schema("col_binary", "binary(8388608)"),
        Schema("col_varbinary", "binary(8388608)"),
        Schema("col_int", "number(38,0)"),
        Schema("col_bigint", "number(38,0)"),
        Schema("col_smallint", "number(38,0)"),
        Schema("col_float", "float"),
        Schema("col_float4", "float"),
        Schema("col_double", "float"),
        Schema("col_real", "float"),
        Schema("col_date", "date"),
        Schema("col_time", "time(9)"),
        Schema("col_timestamp", "timestamp_ntz(9)"),
        Schema("col_timestamp_ltz", "timestamp_ltz(9)"),
        Schema("col_timestamp_ntz", "timestamp_ntz(9)"),
        Schema("col_timestamp_tz", "timestamp_tz(9)"),
        Schema("col_variant", "variant"),
        Schema("col_object", "object"),
        Schema("col_array", "array"),
        Schema("col_geography", "geography"),
        Schema("col_num10", "number(10,1)"),
        Schema("col_dec", "number(20,2)"),
        Schema("col_numeric_2", "numeric(38,0)"),
        Schema("dummy", "string"),
    ]
    tgt_schema = [
        Schema("col_boolean", "boolean"),
        Schema("char", "string"),
        Schema("col_varchar", "string"),
        Schema("col_string", "string"),
        Schema("col_text", "string"),
        Schema("col_binary", "binary"),
        Schema("col_varbinary", "binary"),
        Schema("col_int", "decimal(38,0)"),
        Schema("col_bigint", "decimal(38,0)"),
        Schema("col_smallint", "decimal(38,0)"),
        Schema("col_float", "double"),
        Schema("col_float4", "double"),
        Schema("col_double", "double"),
        Schema("col_real", "double"),
        Schema("col_date", "date"),
        Schema("col_time", "timestamp"),
        Schema("col_timestamp", "timestamp"),
        Schema("col_timestamp_ltz", "timestamp"),
        Schema("col_timestamp_ntz", "timestamp_ntz"),
        Schema("col_timestamp_tz", "timestamp"),
        Schema("col_variant", "string"),
        Schema("col_object", "string"),
        Schema("array_col", "array<string>"),
        Schema("col_geography", "string"),
        Schema("col_num10", "decimal(10,1)"),
        Schema("col_dec", "decimal(20,1)"),
        Schema("col_numeric_2", "decimal(38,0)"),
    ]
    return src_schema, tgt_schema


@pytest.fixture
def databricks_databricks_schema():
    src_schema = [
        Schema("col_boolean", "boolean"),
        Schema("col_char", "string"),
        Schema("col_int", "int"),
        Schema("col_string", "string"),
        Schema("col_bigint", "bigint"),
        Schema("col_num10", "decimal(10,1)"),
        Schema("col_dec", "decimal(20,2)"),
        Schema("col_numeric_2", "decimal(38,0)"),
        Schema("dummy", "string"),
    ]
    tgt_schema = [
        Schema("col_boolean", "boolean"),
        Schema("char", "string"),
        Schema("col_int", "int"),
        Schema("col_string", "string"),
        Schema("col_bigint", "int"),
        Schema("col_num10", "decimal(10,1)"),
        Schema("col_dec", "decimal(20,1)"),
        Schema("col_numeric_2", "decimal(38,0)"),
    ]
    return src_schema, tgt_schema


@pytest.fixture
def oracle_databricks_schema():
    src_schema = [
        Schema("col_xmltype", "xmltype"),
        Schema("col_char", "char(1)"),
        Schema("col_nchar", "nchar(255)"),
        Schema("col_varchar", "varchar2(255)"),
        Schema("col_varchar2", "varchar2(255)"),
        Schema("col_nvarchar", "nvarchar2(255)"),
        Schema("col_nvarchar2", "nvarchar2(255)"),
        Schema("col_character", "char(255)"),
        Schema("col_clob", "clob"),
        Schema("col_nclob", "nclob"),
        Schema("col_long", "long"),
        Schema("col_number", "number(10,2)"),
        Schema("col_float", "float"),
        Schema("col_binary_float", "binary_float"),
        Schema("col_binary_double", "binary_double"),
        Schema("col_date", "date"),
        Schema("col_timestamp", "timestamp(6)"),
        Schema("col_time_with_tz", "timestamp(6) with time zone"),
        Schema("col_timestamp_with_tz", "timestamp(6) with time zone"),
        Schema("col_timestamp_with_local_tz", "timestamp(6) with local time zone"),
        Schema("col_blob", "blob"),
        Schema("col_rowid", "rowid"),
        Schema("col_urowid", "urowid"),
        Schema("col_anytype", "anytype"),
        Schema("col_anydata", "anydata"),
        Schema("col_anydataset", "anydataset"),
        Schema("dummy", "string"),
    ]

    tgt_schema = [
        Schema("col_xmltype", "string"),
        Schema("char", "string"),
        Schema("col_nchar", "string"),
        Schema("col_varchar", "string"),
        Schema("col_varchar2", "string"),
        Schema("col_nvarchar", "string"),
        Schema("col_nvarchar2", "string"),
        Schema("col_character", "string"),
        Schema("col_clob", "string"),
        Schema("col_nclob", "string"),
        Schema("col_long", "string"),
        Schema("col_number", "DECIMAL(10,2)"),
        Schema("col_float", "double"),
        Schema("col_binary_float", "double"),
        Schema("col_binary_double", "double"),
        Schema("col_date", "date"),
        Schema("col_timestamp", "timestamp"),
        Schema("col_time_with_tz", "timestamp"),
        Schema("col_timestamp_with_tz", "timestamp"),
        Schema("col_timestamp_with_local_tz", "timestamp"),
        Schema("col_blob", "binary"),
        Schema("col_rowid", "string"),
        Schema("col_urowid", "string"),
        Schema("col_anytype", "string"),
        Schema("col_anydata", "string"),
        Schema("col_anydataset", "string"),
    ]

    return src_schema, tgt_schema
