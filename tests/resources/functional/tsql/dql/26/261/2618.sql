-- tsql sql:
WITH temp_result AS (SELECT GETDATE() AS [current_date], @@CONNECTIONS AS login_attempts)
SELECT [current_date] AS 'Current Date and Time',
       login_attempts AS 'Total Login Attempts'
FROM temp_result
