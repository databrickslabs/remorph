
-- snowflake sql:
SELECT nvl2(cond, col1, col2) AS nvl2_col1 FROM tabl;

-- databricks sql:
SELECT NVL2(cond, col1, col2) AS nvl2_col1 FROM tabl;
