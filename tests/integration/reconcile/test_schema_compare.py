import pytest

from databricks.labs.remorph.reconcile.dialects.utils import get_dialect
from databricks.labs.remorph.reconcile.recon_config import ColumnMapping, ColumnType, TableMapping
from databricks.labs.remorph.reconcile.schema_compare import SchemaCompare


def snowflake_databricks_schema():
    src_schema = [
        ColumnType("col_boolean", "boolean"),
        ColumnType("col_char", "varchar(1)"),
        ColumnType("col_varchar", "varchar(16777216)"),
        ColumnType("col_string", "varchar(16777216)"),
        ColumnType("col_text", "varchar(16777216)"),
        ColumnType("col_binary", "binary(8388608)"),
        ColumnType("col_varbinary", "binary(8388608)"),
        ColumnType("col_int", "number(38,0)"),
        ColumnType("col_bigint", "number(38,0)"),
        ColumnType("col_smallint", "number(38,0)"),
        ColumnType("col_float", "float"),
        ColumnType("col_float4", "float"),
        ColumnType("col_double", "float"),
        ColumnType("col_real", "float"),
        ColumnType("col_date", "date"),
        ColumnType("col_time", "time(9)"),
        ColumnType("col_timestamp", "timestamp_ntz(9)"),
        ColumnType("col_timestamp_ltz", "timestamp_ltz(9)"),
        ColumnType("col_timestamp_ntz", "timestamp_ntz(9)"),
        ColumnType("col_timestamp_tz", "timestamp_tz(9)"),
        ColumnType("col_variant", "variant"),
        ColumnType("col_object", "object"),
        ColumnType("col_array", "array"),
        ColumnType("col_geography", "geography"),
        ColumnType("col_num10", "number(10,1)"),
        ColumnType("col_dec", "number(20,2)"),
        ColumnType("col_numeric_2", "numeric(38,0)"),
        ColumnType("dummy", "string"),
    ]
    tgt_schema = [
        ColumnType("col_boolean", "boolean"),
        ColumnType("char", "string"),
        ColumnType("col_varchar", "string"),
        ColumnType("col_string", "string"),
        ColumnType("col_text", "string"),
        ColumnType("col_binary", "binary"),
        ColumnType("col_varbinary", "binary"),
        ColumnType("col_int", "decimal(38,0)"),
        ColumnType("col_bigint", "decimal(38,0)"),
        ColumnType("col_smallint", "decimal(38,0)"),
        ColumnType("col_float", "double"),
        ColumnType("col_float4", "double"),
        ColumnType("col_double", "double"),
        ColumnType("col_real", "double"),
        ColumnType("col_date", "date"),
        ColumnType("col_time", "timestamp"),
        ColumnType("col_timestamp", "timestamp_ntz"),
        ColumnType("col_timestamp_ltz", "timestamp"),
        ColumnType("col_timestamp_ntz", "timestamp_ntz"),
        ColumnType("col_timestamp_tz", "timestamp"),
        ColumnType("col_variant", "variant"),
        ColumnType("col_object", "string"),
        ColumnType("array_col", "array<string>"),
        ColumnType("col_geography", "string"),
        ColumnType("col_num10", "decimal(10,1)"),
        ColumnType("col_dec", "decimal(20,1)"),
        ColumnType("col_numeric_2", "decimal(38,0)"),
    ]
    return src_schema, tgt_schema


def databricks_databricks_schema():
    src_schema = [
        ColumnType("col_boolean", "boolean"),
        ColumnType("col_char", "string"),
        ColumnType("col_int", "int"),
        ColumnType("col_string", "string"),
        ColumnType("col_bigint", "int"),
        ColumnType("col_num10", "decimal(10,1)"),
        ColumnType("col_dec", "decimal(20,2)"),
        ColumnType("col_numeric_2", "decimal(38,0)"),
        ColumnType("dummy", "string"),
    ]
    tgt_schema = [
        ColumnType("col_boolean", "boolean"),
        ColumnType("char", "string"),
        ColumnType("col_int", "int"),
        ColumnType("col_string", "string"),
        ColumnType("col_bigint", "int"),
        ColumnType("col_num10", "decimal(10,1)"),
        ColumnType("col_dec", "decimal(20,1)"),
        ColumnType("col_numeric_2", "decimal(38,0)"),
    ]
    return src_schema, tgt_schema


def oracle_databricks_schema():
    src_schema = [
        ColumnType("col_xmltype", "xmltype"),
        ColumnType("col_char", "char(1)"),
        ColumnType("col_nchar", "nchar(255)"),
        ColumnType("col_varchar", "varchar2(255)"),
        ColumnType("col_varchar2", "varchar2(255)"),
        ColumnType("col_nvarchar", "nvarchar2(255)"),
        ColumnType("col_nvarchar2", "nvarchar2(255)"),
        ColumnType("col_character", "char(255)"),
        ColumnType("col_clob", "clob"),
        ColumnType("col_nclob", "nclob"),
        ColumnType("col_long", "long"),
        ColumnType("col_number", "number(10,2)"),
        ColumnType("col_float", "float"),
        ColumnType("col_binary_float", "binary_float"),
        ColumnType("col_binary_double", "binary_double"),
        ColumnType("col_date", "date"),
        ColumnType("col_timestamp", "timestamp(6)"),
        ColumnType("col_time_with_tz", "timestamp(6) with time zone"),
        ColumnType("col_timestamp_with_tz", "timestamp(6) with time zone"),
        ColumnType("col_timestamp_with_local_tz", "timestamp(6) with local time zone"),
        ColumnType("col_blob", "blob"),
        ColumnType("col_rowid", "rowid"),
        ColumnType("col_urowid", "urowid"),
        ColumnType("col_anytype", "anytype"),
        ColumnType("col_anydata", "anydata"),
        ColumnType("col_anydataset", "anydataset"),
        ColumnType("dummy", "string"),
    ]

    tgt_schema = [
        ColumnType("col_xmltype", "string"),
        ColumnType("char", "string"),
        ColumnType("col_nchar", "string"),
        ColumnType("col_varchar", "string"),
        ColumnType("col_varchar2", "string"),
        ColumnType("col_nvarchar", "string"),
        ColumnType("col_nvarchar2", "string"),
        ColumnType("col_character", "string"),
        ColumnType("col_clob", "string"),
        ColumnType("col_nclob", "string"),
        ColumnType("col_long", "string"),
        ColumnType("col_number", "DECIMAL(10,2)"),
        ColumnType("col_float", "double"),
        ColumnType("col_binary_float", "double"),
        ColumnType("col_binary_double", "double"),
        ColumnType("col_date", "date"),
        ColumnType("col_timestamp", "timestamp"),
        ColumnType("col_time_with_tz", "timestamp"),
        ColumnType("col_timestamp_with_tz", "timestamp"),
        ColumnType("col_timestamp_with_local_tz", "timestamp"),
        ColumnType("col_blob", "binary"),
        ColumnType("col_rowid", "string"),
        ColumnType("col_urowid", "string"),
        ColumnType("col_anytype", "string"),
        ColumnType("col_anydata", "string"),
        ColumnType("col_anydataset", "string"),
    ]

    return src_schema, tgt_schema


@pytest.fixture
def schemas():
    return {
        "snowflake_databricks_schema": snowflake_databricks_schema(),
        "databricks_databricks_schema": databricks_databricks_schema(),
        "oracle_databricks_schema": oracle_databricks_schema(),
    }


def test_snowflake_schema_compare(schemas, mock_spark):
    src_schema, tgt_schema = schemas["snowflake_databricks_schema"]
    spark = mock_spark
    table_mapping = TableMapping(
        source_name="supplier",
        target_name="supplier",
        drop_columns=["dummy"],
        column_mapping=[
            ColumnMapping(source_name="col_char", target_name="char"),
            ColumnMapping(source_name="col_array", target_name="array_col"),
        ],
    )

    schema_compare_output = SchemaCompare(spark).compare(
        src_schema,
        tgt_schema,
        get_dialect("snowflake"),
        table_mapping,
    )
    df = schema_compare_output.compare_df

    assert not schema_compare_output.is_valid
    assert df.count() == 27
    assert df.filter("is_valid = 'true'").count() == 25
    assert df.filter("is_valid = 'false'").count() == 2


def test_databricks_schema_compare(schemas, mock_spark):
    src_schema, tgt_schema = schemas["databricks_databricks_schema"]
    spark = mock_spark
    table_mapping = TableMapping(
        source_name="supplier",
        target_name="supplier",
        select_columns=[
            "col_boolean",
            "col_char",
            "col_int",
            "col_string",
            "col_bigint",
            "col_num10",
            "col_dec",
            "col_numeric_2",
        ],
        column_mapping=[
            ColumnMapping(source_name="col_char", target_name="char"),
            ColumnMapping(source_name="col_array", target_name="array_col"),
        ],
    )
    schema_compare_output = SchemaCompare(spark).compare(
        src_schema,
        tgt_schema,
        get_dialect("databricks"),
        table_mapping,
    )
    df = schema_compare_output.compare_df

    assert not schema_compare_output.is_valid
    assert df.count() == 8
    assert df.filter("is_valid = 'true'").count() == 7
    assert df.filter("is_valid = 'false'").count() == 1


def test_oracle_schema_compare(schemas, mock_spark):
    src_schema, tgt_schema = schemas["oracle_databricks_schema"]
    spark = mock_spark
    table_mapping = TableMapping(
        source_name="supplier",
        target_name="supplier",
        drop_columns=["dummy"],
        column_mapping=[
            ColumnMapping(source_name="col_char", target_name="char"),
            ColumnMapping(source_name="col_array", target_name="array_col"),
        ],
    )
    schema_compare_output = SchemaCompare(spark).compare(
        src_schema,
        tgt_schema,
        get_dialect("oracle"),
        table_mapping,
    )
    df = schema_compare_output.compare_df

    assert schema_compare_output.is_valid
    assert df.count() == 26
    assert df.filter("is_valid = 'true'").count() == 26
    assert df.filter("is_valid = 'false'").count() == 0


def test_schema_compare(mock_spark):
    src_schema = [
        ColumnType("col1", "int"),
        ColumnType("col2", "string"),
    ]
    tgt_schema = [
        ColumnType("col1", "int"),
        ColumnType("col2", "string"),
    ]
    spark = mock_spark
    table_mapping = TableMapping(
        source_name="supplier",
        target_name="supplier",
        drop_columns=["dummy"],
        column_mapping=[
            ColumnMapping(source_name="col_char", target_name="char"),
            ColumnMapping(source_name="col_array", target_name="array_col"),
        ],
    )

    schema_compare_output = SchemaCompare(spark).compare(
        src_schema,
        tgt_schema,
        get_dialect("databricks"),
        table_mapping,
    )
    df = schema_compare_output.compare_df

    assert schema_compare_output.is_valid
    assert df.count() == 2
    assert df.filter("is_valid = 'true'").count() == 2
    assert df.filter("is_valid = 'false'").count() == 0
