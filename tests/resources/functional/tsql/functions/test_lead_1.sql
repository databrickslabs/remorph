-- ## LEAD
--
-- The LEAD function is identical in TSql and Databricks.

-- tsql sql:
SELECT col1, col2, LEAD(col2, 1, 0) OVER (ORDER BY col2 DESC) AS lead_value FROM tabl;

-- databricks sql:
SELECT col1, col2, LEAD(col2, 1, 0) OVER (ORDER BY col2 DESC) AS lead_value FROM tabl;
