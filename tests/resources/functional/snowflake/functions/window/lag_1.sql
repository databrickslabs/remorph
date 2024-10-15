-- snowflake sql:
SELECT
  lag(col1) OVER (
    PARTITION BY col1
    ORDER BY
      col2
  ) AS lag_col1
FROM
  tabl;

-- databricks sql:
SELECT
  LAG(col1) OVER (
    PARTITION BY col1
    ORDER BY
      col2 ASC NULLS LAST
  ) AS lag_col1
FROM
  tabl;
