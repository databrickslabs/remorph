
-- snowflake sql:
SELECT date_trunc('MM', col1) AS date_trunc_col1 FROM tabl;

-- databricks sql:
SELECT DATE_TRUNC('MONTH', col1) AS date_trunc_col1 FROM tabl;
