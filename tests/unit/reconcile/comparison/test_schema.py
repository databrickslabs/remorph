from databricks.labs.remorph.reconcile.comparison.schema import SchemaCompare
from databricks.labs.remorph.reconcile.recon_config import ColumnMapping, Table


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

    result, df = SchemaCompare(src_schema, tgt_schema, "snowflake", table_conf, spark).compare()
    print(f"Result: {result}")
    df.show(100, truncate=False)

    assert result == "Failed"
    assert df.count() == 27
    assert df.filter("is_valid = 'true'").count() == 24
    assert df.filter("is_valid = 'false'").count() == 3


def test_databricks_schema_compare(databricks_databricks_schema, mock_spark_session):
    src_schema, tgt_schema = databricks_databricks_schema
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
    result, df = SchemaCompare(src_schema, tgt_schema, "databricks", table_conf, spark).compare()
    print(f"Result: {result}")
    df.show(100, truncate=False)

    assert result == "Failed"
    assert df.count() == 8
    assert df.filter("is_valid = 'true'").count() == 6
    assert df.filter("is_valid = 'false'").count() == 2


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
    result, df = SchemaCompare(src_schema, tgt_schema, "oracle", table_conf, spark).compare()
    print(f"Result: {result}")
    df.show(100, truncate=False)

    assert result == "Failed"
    assert df.count() == 26
    assert df.filter("is_valid = 'true'").count() == 18
    assert df.filter("is_valid = 'false'").count() == 8
