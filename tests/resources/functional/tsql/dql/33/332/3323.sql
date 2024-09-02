--Query type: DQL
WITH temp_result AS (SELECT SYSDATETIME() AS [current_time])
SELECT temp_result.[current_time]
FROM temp_result