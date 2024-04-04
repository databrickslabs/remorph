
-- snowflake sql:
SELECT array_slice(array_construct(90,91,92,93,94,95,96), -5, 3);

-- databricks sql:
SELECT SLICE(ARRAY(90, 91, 92, 93, 94, 95, 96), -5, 3);
