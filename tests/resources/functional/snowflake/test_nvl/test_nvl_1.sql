
-- snowflake sql:
SELECT nvl(col1, col2) AS nvl_col FROM tabl;

-- databricks sql:
SELECT COALESCE(col1, col2) AS nvl_col FROM tabl;
