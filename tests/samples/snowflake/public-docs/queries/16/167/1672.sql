-- see https://docs.snowflake.com/en/sql-reference/functions/floor

SELECT n, scale, FLOOR(n, scale)
  FROM test_floor
  ORDER BY n, scale;