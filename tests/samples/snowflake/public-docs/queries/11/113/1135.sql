-- see https://docs.snowflake.com/en/sql-reference/functions/trunc

SELECT DISTINCT n, TRUNCATE(n) 
  FROM test_1
  ORDER BY n;