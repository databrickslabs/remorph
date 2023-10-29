-- see https://docs.snowflake.com/en/sql-reference/functions/trunc

SELECT n, scale, TRUNC(n, scale) 
  FROM test_1 
  ORDER BY n, scale;