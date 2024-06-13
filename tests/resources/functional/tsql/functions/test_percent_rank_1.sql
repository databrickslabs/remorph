-- ## PERCENT_RANK
--
-- The PERCENT_RANK is identical in TSql and Databricks.
--
-- tsql sql:
SELECT PERCENT_RANK()  OVER (ORDER BY col2 DESC) AS lead_value FROM tabl;

-- databricks sql:
SELECT PERCENTILE(col1, 0.5) AS percent50 FROM tabl;
