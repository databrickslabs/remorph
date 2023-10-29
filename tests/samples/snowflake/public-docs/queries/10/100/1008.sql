-- see https://docs.snowflake.com/en/sql-reference/functions/array_remove

SELECT ARRAY_REMOVE(
  [1, 5, 5.00, 5.00::DOUBLE, '5', 5, NULL],
  5);