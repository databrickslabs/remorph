from databricks.labs.remorph.reconcile.recon_config import ColumnMapping, Schema, Table
from databricks.labs.remorph.reconcile.schema_compare import SchemaCompare


def test_snowflake_schema_compare(snowflake_databricks_schema, mock_spark_session):
    src_schema, tgt_schema = snowflake_databricks_schema
    spark = mock_spark_session
    table_conf = Table(
        source_name="supplier",
        target_name="supplier",
        drop_columns=["dummy"],
        column_mapping=[
            ColumnMapping(source_name="col_char", target_name="char"),
            ColumnMapping(source_name="col_array", target_name="array_col"),
        ],
    )

    schema_compare_output = SchemaCompare(src_schema, tgt_schema, "snowflake", table_conf, spark).compare()
    df = schema_compare_output.compare_df
    df.show(100, truncate=False)

    assert not schema_compare_output.is_valid
    assert df.count() == 27
    assert df.filter("is_valid = 'true'").count() == 25
    assert df.filter("is_valid = 'false'").count() == 2


def test_databricks_schema_compare(databricks_databricks_schema, mock_spark_session):
    src_schema, tgt_schema = databricks_databricks_schema
    spark = mock_spark_session
    table_conf = Table(
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
    schema_compare_output = SchemaCompare(src_schema, tgt_schema, "databricks", table_conf, spark).compare()
    df = schema_compare_output.compare_df
    df.show(100, truncate=False)

    assert not schema_compare_output.is_valid
    assert df.count() == 8
    assert df.filter("is_valid = 'true'").count() == 7
    assert df.filter("is_valid = 'false'").count() == 1


def test_oracle_schema_compare(oracle_databricks_schema, mock_spark_session):
    src_schema, tgt_schema = oracle_databricks_schema
    spark = mock_spark_session
    table_conf = Table(
        source_name="supplier",
        target_name="supplier",
        drop_columns=["dummy"],
        column_mapping=[
            ColumnMapping(source_name="col_char", target_name="char"),
            ColumnMapping(source_name="col_array", target_name="array_col"),
        ],
    )
    schema_compare_output = SchemaCompare(src_schema, tgt_schema, "oracle", table_conf, spark).compare()
    df = schema_compare_output.compare_df
    df.show(100, truncate=False)

    assert not schema_compare_output.is_valid
    assert df.count() == 26
    assert df.filter("is_valid = 'true'").count() == 19
    assert df.filter("is_valid = 'false'").count() == 7


def test_schema_compare(mock_spark_session):
    src_schema = [
        Schema("col1", "int"),
        Schema("col2", "string"),
    ]
    tgt_schema = [
        Schema("col1", "int"),
        Schema("col2", "string"),
    ]
    spark = mock_spark_session
    table_conf = Table(
        source_name="supplier",
        target_name="supplier",
        drop_columns=["dummy"],
        column_mapping=[
            ColumnMapping(source_name="col_char", target_name="char"),
            ColumnMapping(source_name="col_array", target_name="array_col"),
        ],
    )

    schema_compare_output = SchemaCompare(src_schema, tgt_schema, "databricks", table_conf, spark).compare()
    df = schema_compare_output.compare_df
    df.show(100, truncate=False)

    assert schema_compare_output.is_valid
    assert df.count() == 2
    assert df.filter("is_valid = 'true'").count() == 2
    assert df.filter("is_valid = 'false'").count() == 0
