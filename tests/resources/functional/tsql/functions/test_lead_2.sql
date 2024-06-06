-- ## LEAD ignoring NULL values
--
-- The LEAD function is identical in TSql and Databricks when IGNORING or RESPECTING NULLS (default).

-- tsql sql:
SELECT col1, col2, LEAD(col2, 1, 0) IGNORE NULLS OVER (ORDER BY col2 DESC) AS lead_value FROM tabl;

-- databricks sql:
SELECT col1, col2, LEAD(col2, 1, 0) IGNORE NULLS OVER (ORDER BY col2 DESC) AS lead_value FROM tabl;
