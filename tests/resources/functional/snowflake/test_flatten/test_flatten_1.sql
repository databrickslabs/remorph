
-- source:
SELECT flatten(col1) AS flatten_col1 FROM tabl;

-- databricks_sql:
SELECT EXPLODE(col1) AS flatten_col1 FROM tabl;
