-- see https://docs.snowflake.com/en/sql-reference/functions/round

SELECT n, scale, ROUND(n, scale)
  FROM test_ceiling
  ORDER BY n, scale;