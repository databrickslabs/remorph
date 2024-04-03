
-- source:
SELECT nvl(col1, col2) AS nvl_col FROM tabl;

-- databricks_sql:
SELECT COALESCE(col1, col2) AS nvl_col FROM tabl;
