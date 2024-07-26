
-- snowflake sql:
SELECT iff(cond, col1, col2) AS iff_col1 FROM tabl;

-- databricks sql:
SELECT IF(cond, col1, col2) AS iff_col1 FROM tabl;
