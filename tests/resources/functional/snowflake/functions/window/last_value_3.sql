-- snowflake sql:
SELECT
  last_value(col1) AS last_value_col1
FROM
  tabl;

-- databricks sql:
SELECT
  LAST_VALUE(col1) AS last_value_col1
FROM
  tabl;