-- snowflake sql:
SELECT
  rank() over (
    partition by col1
    order by
      col2
  ) AS rank_col1
FROM
  tabl;

-- databricks sql:
SELECT
  RANK() OVER (
    PARTITION BY col1
    ORDER BY
      col2 ASC NULLS LAST
  ) AS rank_col1
FROM
  tabl;
