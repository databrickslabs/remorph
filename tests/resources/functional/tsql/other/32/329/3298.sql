-- tsql sql:
WITH AppInfo AS (
    SELECT APP_NAME() AS AppName,
           CONVERT(VARCHAR(100), GETDATE(), 101) AS Date101,
           CONVERT(VARCHAR(100), GETDATE(), 102) AS Date102
)
SELECT CASE
        WHEN AppName = 'Microsoft SQL Server Management Studio - Query'
            THEN 'This process was started by ' + AppName + '. The date is ' + Date101 + '.'
        ELSE 'This process was started by ' + AppName + '. The date is ' + Date102 + '.'
    END AS Message
FROM AppInfo;
