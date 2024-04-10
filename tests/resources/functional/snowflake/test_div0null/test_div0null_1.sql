
-- snowflake sql:
SELECT DIV0NULL(a, b);

-- databricks sql:
SELECT IF(b = 0 OR b IS NULL, 0, a / b);
