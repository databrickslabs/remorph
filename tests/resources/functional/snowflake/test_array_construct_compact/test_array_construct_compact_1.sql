
-- source:
SELECT ARRAY_CONSTRUCT(null, 'hello', 3::double, 4, 5);

-- databricks_sql:
SELECT ARRAY(NULL, 'hello', CAST(3 AS DOUBLE), 4, 5);
