--Query type: DCL
WITH temp_result AS (SELECT 'value1' AS column1, 'value2' AS column2), temp_result2 AS (SELECT 'value3' AS column1, 'value4' AS column2 UNION ALL SELECT 'value5', 'value6') SELECT * FROM temp_result UNION ALL SELECT * FROM temp_result2
