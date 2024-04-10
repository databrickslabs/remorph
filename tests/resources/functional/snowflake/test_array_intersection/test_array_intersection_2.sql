
-- snowflake sql:
SELECT ARRAY_INTERSECTION(ARRAY_CONSTRUCT(1, 2, 3), ARRAY_CONSTRUCT(1, 2));

-- databricks sql:
SELECT ARRAY_INTERSECT(ARRAY(1, 2, 3), ARRAY(1, 2));
