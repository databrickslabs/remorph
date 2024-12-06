-- tsql sql:
WITH ModifiedDatabase AS (
    SELECT DatabaseName, State, FileGroupName, MaxSizeGB
    FROM #DatabaseProperties
    WHERE DatabaseName = 'CustomerSales'
)
SELECT 'ALTER DATABASE ' + DatabaseName + ' SET ONLINE;' AS Query
FROM ModifiedDatabase
WHERE State = 6
UNION ALL
SELECT 'ALTER DATABASE ' + DatabaseName + ' MODIFY FILEGROUP ' + FileGroupName + ' (MAXSIZE = ' + CONVERT(varchar, MaxSizeGB) + ' GB);' AS Query
FROM ModifiedDatabase;
SELECT * FROM #DatabaseProperties;
