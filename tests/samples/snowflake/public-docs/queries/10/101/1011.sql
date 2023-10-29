-- see https://docs.snowflake.com/en/sql-reference/functions/array_remove_at

SELECT ARRAY_REMOVE_AT(
  [2, 5, 7],
  0);