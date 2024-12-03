--Query type: DDL
IF OBJECT_ID('temp_result', 'U') IS NOT NULL
    DROP TABLE temp_result;

WITH temp_result AS (
    SELECT 1 AS id, 'test' AS name
)
SELECT *
FROM temp_result;
