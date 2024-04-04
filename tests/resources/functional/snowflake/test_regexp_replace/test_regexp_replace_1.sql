
-- source:
SELECT regexp_replace(col1, '(d+)', '***') AS regexp_replace_col1 FROM tabl;

-- databricks_sql:
SELECT REGEXP_REPLACE(col1, '(d+)', '***') AS regexp_replace_col1 FROM tabl;
