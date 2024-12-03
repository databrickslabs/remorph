--Query type: DQL
WITH temp_result AS (SELECT 1 AS month, SYSDATETIME() AS [current_date])
SELECT DATEADD(month, month, [current_date]) AS new_date
FROM temp_result
