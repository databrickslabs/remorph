-- see https://docs.snowflake.com/en/sql-reference/functions/approx_count_distinct

SELECT COUNT(i), COUNT(DISTINCT i), APPROX_COUNT_DISTINCT(i), HLL(i)
  FROM sequence_demo;