-- see https://docs.snowflake.com/en/sql-reference/functions/ceil

SELECT n, scale, ceil(n, scale)
  FROM test_ceiling
  ORDER BY n, scale;