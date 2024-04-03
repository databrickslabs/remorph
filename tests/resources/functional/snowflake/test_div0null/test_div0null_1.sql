
-- source:
SELECT DIV0NULL(a, b);

-- databricks_sql:
SELECT IF(b = 0 OR b IS NULL, 0, a / b);
