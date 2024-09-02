--Query type: DQL
WITH temp_result AS (SELECT 'value1' AS column_1, 'value2' AS column_2)
SELECT column_1, column_2
FROM temp_result;