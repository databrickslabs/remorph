--Query type: DQL
WITH temp_result AS (SELECT 'abc[]def' AS str)
SELECT QUOTENAME(str)
FROM temp_result;