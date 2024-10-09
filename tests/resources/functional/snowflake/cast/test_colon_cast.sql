-- snowflake sql:
SELECT
    ARRAY_REMOVE([2, 3, 4::DOUBLE, 4, NULL], 4)

-- databricks sql:
SELECT
    ARRAY_REMOVE(ARRAY(2, 3, CAST(4 AS DOUBLE), 4, NULL), 4);
