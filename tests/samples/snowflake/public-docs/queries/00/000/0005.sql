-- see https://docs.snowflake.com/en/sql-reference/functions/infer_schema

-- Create a file format that sets the file type as JSON.
CREATE FILE FORMAT my_json_format
  TYPE = json;

-- Query the INFER_SCHEMA function.
SELECT *
  FROM TABLE(
    INFER_SCHEMA(
      LOCATION=>'@mystage/json/'
      , FILE_FORMAT=>'my_json_format'
      )
    );
