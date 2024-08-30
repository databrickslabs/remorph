
-- snowflake sql:
SELECT approx_percentile(col1, 0.5) AS approx_percentile_col1 FROM tabl;

-- databricks sql:
SELECT APPROX_PERCENTILE(col1, 0.5) AS approx_percentile_col1 FROM tabl;
