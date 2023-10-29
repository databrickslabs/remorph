-- see https://docs.snowflake.com/en/sql-reference/functions/hll

SELECT COUNT(i), COUNT(DISTINCT i), APPROX_COUNT_DISTINCT(i), HLL(i)
  FROM sequence_demo;