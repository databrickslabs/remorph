-- see https://docs.snowflake.com/en/sql-reference/functions/generate_column_description

-- Query the GENERATE_COLUMN_DESCRIPTION function.
SELECT GENERATE_COLUMN_DESCRIPTION(ARRAY_AGG(OBJECT_CONSTRUCT(*)), 'external_table') AS COLUMNS
  FROM TABLE (
    INFER_SCHEMA(
      LOCATION=>'@mystage',
      FILE_FORMAT=>'my_parquet_format'
    )
  );
