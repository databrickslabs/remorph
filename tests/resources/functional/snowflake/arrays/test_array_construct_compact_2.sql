
-- snowflake sql:
SELECT ARRAY_CONSTRUCT_COMPACT(null, 'hello', 3::double, 4, 5);

-- databricks sql:
SELECT ARRAY_EXCEPT(ARRAY(NULL, 'hello', CAST(3 AS DOUBLE), 4, 5), ARRAY(NULL));
