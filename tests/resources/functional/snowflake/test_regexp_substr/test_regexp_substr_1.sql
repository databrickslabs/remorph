
-- source:
SELECT regexp_substr(col1, '(E|e)rror') AS regexp_substr_col1 FROM tabl;

-- databricks_sql:
SELECT REGEXP_EXTRACT(col1, '(E|e)rror') AS regexp_substr_col1 FROM tabl;
