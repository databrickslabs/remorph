
-- snowflake sql:
SELECT array_slice(array_construct(0,1,2,3,4,5,6), 0, 2);

-- databricks sql:
SELECT SLICE(ARRAY(0, 1, 2, 3, 4, 5, 6), 1, 2);
