-- see https://docs.snowflake.com/en/sql-reference/functions/array_remove

SELECT ARRAY_REMOVE(
  ['a', 'b', 'a', 'c', 'd', 'a'],
  'a'::VARIANT);