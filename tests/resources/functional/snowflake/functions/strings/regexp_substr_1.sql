
-- snowflake sql:
SELECT regexp_substr(col1, '(E|e)rror') AS regexp_substr_col1 FROM tabl;

-- databricks sql:
SELECT REGEXP_EXTRACT(col1, '(E|e)rror', 0) AS regexp_substr_col1 FROM tabl;
