-- snowflake sql:
SELECT
  rank() over (
    partition by col1
    order by
      col2 DESC RANGE BETWEEN UNBOUNDED PRECEDING
      AND CURRENT ROW
  ) AS rank_col1
FROM
  tabl;

-- databricks sql:
SELECT
  RANK() OVER (
    PARTITION BY col1
    ORDER BY
      col2 DESC NULLS FIRST RANGE BETWEEN UNBOUNDED PRECEDING
      AND CURRENT ROW
  ) AS rank_col1
FROM
  tabl;
