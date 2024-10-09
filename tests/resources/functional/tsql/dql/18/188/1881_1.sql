--Query type: DQL
WITH temp_result AS (SELECT 1 AS id)
SELECT GETDATE() AS current_datetime
FROM temp_result