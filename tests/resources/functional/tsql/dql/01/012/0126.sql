-- tsql sql:
WITH temp_result AS (SELECT GETDATE() AS [current_date], CURRENT_TIMESTAMP AS [current_timestamp])
SELECT [current_date], [current_timestamp]
FROM temp_result
