
-- snowflake sql:
SELECT ntile(col1)  OVER (PARTITION BY col1 ORDER BY col2) AS ntile_col1 FROM tabl;

-- databricks sql:
SELECT NTILE(col1) OVER (PARTITION BY col1 ORDER BY col2 NULLS LAST) AS ntile_col1 FROM tabl;
