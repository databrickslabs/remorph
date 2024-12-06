-- snowflake sql:
SELECT
  lag(col1) OVER (
    PARTITION BY col1
    ORDER BY
      col2 DESC RANGE BETWEEN UNBOUNDED PRECEDING
      AND CURRENT ROW
  ) AS lag_col1
FROM
  tabl;

-- databricks sql:
SELECT
  LAG(col1) OVER (
    PARTITION BY col1
    ORDER BY
      col2 DESC NULLS FIRST RANGE BETWEEN UNBOUNDED PRECEDING
      AND CURRENT ROW
  ) AS lag_col1
FROM
  tabl;
