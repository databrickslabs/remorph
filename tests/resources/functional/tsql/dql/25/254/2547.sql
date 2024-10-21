--Query type: DQL
WITH temp_result AS (SELECT SYSDATETIME() AS [current_date], '2021-12-1' AS date_string)
SELECT DATETRUNC(m, SYSDATETIME()), DATETRUNC(yyyy, CONVERT(date, date_string))
FROM temp_result