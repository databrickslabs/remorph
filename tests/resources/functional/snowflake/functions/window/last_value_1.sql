-- snowflake sql:
SELECT
  last_value(col1) over (
    partition by col1
    order by
      col2
  ) AS last_value_col1
FROM
  tabl;

-- databricks sql:
SELECT
  LAST(col1) OVER (
    PARTITION BY col1
    ORDER BY
      col2 ASC NULLS LAST ROWS BETWEEN UNBOUNDED PRECEDING
      AND UNBOUNDED FOLLOWING
  ) AS last_value_col1
FROM
  tabl;
