-- see https://docs.snowflake.com/en/sql-reference/sql/create-external-table

CREATE EXTERNAL TABLE mytable
  USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
      FROM TABLE(
        INFER_SCHEMA(
          LOCATION=>'@mystage',
          FILE_FORMAT=>'my_parquet_format'
        )
      )
    )
    LOCATION=@mystage
    FILE_FORMAT=my_parquet_format
    AUTO_REFRESH=false;