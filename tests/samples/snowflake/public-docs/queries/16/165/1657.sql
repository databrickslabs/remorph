-- see https://docs.snowflake.com/en/sql-reference/functions/min

SELECT k, d, MAX(d) OVER (ORDER BY k, d ROWS BETWEEN 1 PRECEDING AND CURRENT ROW)
  FROM minmax_example
  ORDER BY k, d;