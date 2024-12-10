-- tsql sql:
WITH temp_result AS (
    SELECT 'value1' AS column1, 'value2' AS column2
    UNION ALL
    SELECT 'value3', 'value4'
)
SELECT *
FROM temp_result;
