-- snowflake sql:
SELECT
  first_value(col1) over (
    partition by col1
    order by
      col2
  ) AS first_value_col1
FROM
  tabl;

-- databricks sql:
SELECT
  FIRST(col1) OVER (
    PARTITION BY col1
    ORDER BY
      col2 ASC NULLS LAST ROWS BETWEEN UNBOUNDED PRECEDING
      AND UNBOUNDED FOLLOWING
  ) AS first_value_col1
FROM
  tabl;
