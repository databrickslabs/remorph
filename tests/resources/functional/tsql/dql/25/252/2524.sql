--Query type: DQL
WITH [current_date] AS (SELECT CAST(SYSDATETIME() AS datetime) AS [current_date])
SELECT DATEADD(month, -(10/2), [current_date])
FROM [current_date]