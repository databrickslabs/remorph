
-- source:
SELECT a.col1, CONVERT_TIMEZONE('IST', a.ts_col) AS conv_ts FROM dummy a;

-- databricks_sql:
SELECT a.col1, CONVERT_TIMEZONE('IST', a.ts_col) AS conv_ts FROM dummy AS a;
