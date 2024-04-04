
-- source:
SELECT regexp_like(col1, 'Users.*') AS regexp_like_col1 FROM tabl;

-- databricks_sql:
SELECT col1 RLIKE 'Users.*' AS regexp_like_col1 FROM tabl;
