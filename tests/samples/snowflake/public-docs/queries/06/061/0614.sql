-- see https://docs.snowflake.com/en/sql-reference/functions/result_scan

DESC USER jessicajones;
SELECT "property", "value" FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
  WHERE "property" = 'DEFAULT_ROLE'
  ;