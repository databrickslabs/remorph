
-- source:
SELECT date_trunc('MM', col1) AS date_trunc_col1 FROM tabl;

-- databricks_sql:
SELECT DATE_TRUNC('MONTH', col1) AS date_trunc_col1 FROM tabl;
