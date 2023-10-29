-- see https://docs.snowflake.com/en/sql-reference/functions/infer_schema

-- Query the INFER_SCHEMA function.
SELECT *
  FROM TABLE(
    INFER_SCHEMA(
      LOCATION=>'@mystage'
      , FILE_FORMAT=>'my_parquet_format'
      , IGNORE_CASE=>TRUE
      )
    );
