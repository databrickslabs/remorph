-- see https://docs.snowflake.com/en/sql-reference/functions/infer_schema

-- Create a file format that sets the file type as CSV.
CREATE FILE FORMAT my_csv_format
  TYPE = csv
  PARSE_HEADER = true;

-- Query the INFER_SCHEMA function.
SELECT *
  FROM TABLE(
    INFER_SCHEMA(
      LOCATION=>'@mystage/csv/'
      , FILE_FORMAT=>'my_csv_format'
      )
    );


-- Load the CSV file using MATCH_BY_COLUMN_NAME.
COPY into mytable from @mystage/csv/' FILE_FORMAT = (FORMAT_NAME= 'my_csv_format') MATCH_BY_COLUMN_NAME=CASE_INSENSITIVE;