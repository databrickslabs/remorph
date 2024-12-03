--Query type: DQL
WITH temp_result AS (SELECT 1 AS id)
SELECT CAST(CONVERT(DATETIME, CURRENT_TIMESTAMP) AS TIME) AS time_value
FROM temp_result
