
-- tsql sql:
SELECT DATEADD(MONTH, 1, col1) AS add_months_col1 FROM tabl;

-- databricks sql:
SELECT add_months(col1, 1) AS add_months_col1 FROM tabl;
