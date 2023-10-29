-- see https://docs.snowflake.com/en/sql-reference/functions/min

SELECT k, d, MAX(d) OVER (PARTITION BY k)
  FROM minmax_example
  ORDER BY k, d;