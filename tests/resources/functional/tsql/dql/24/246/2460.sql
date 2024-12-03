--Query type: DQL
WITH temp_result AS (SELECT 'This is a string' AS str)
SELECT CHARINDEX('is', str, 4) AS position
FROM temp_result
