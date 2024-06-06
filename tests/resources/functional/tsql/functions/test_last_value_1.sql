-- ## LAST_VALUE
--
-- The LAST_VALUE function is identical in TSql and Databricks.

-- tsql sql:
SELECT col1, col2, LAST_VALUE(col1) OVER (ORDER BY col2 DESC) AS last_value FROM tabl;

-- databricks sql:
SELECT col1, col2, LAST_VALUE(col1) OVER (ORDER BY col2 DESC) AS last_value FROM tabl;
