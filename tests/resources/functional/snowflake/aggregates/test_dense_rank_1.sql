-- snowflake sql:
SELECT
  dense_rank() OVER (
    PARTITION BY col1
    ORDER BY
      col2
  ) AS dense_rank_col1
FROM
  tabl;

-- databricks sql:
SELECT
  DENSE_RANK() OVER (
    PARTITION BY col1
    ORDER BY
      col2 ASC NULLS LAST ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  ) AS dense_rank_col1
FROM
  tabl;
