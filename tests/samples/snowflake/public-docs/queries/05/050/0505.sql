-- see https://docs.snowflake.com/en/sql-reference/functions/infer_schema

CREATE TABLE mytable
  USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
      FROM TABLE(
        INFER_SCHEMA(
          LOCATION=>'@mystage/json/',
          FILE_FORMAT=>'my_json_format'
        )
      ));