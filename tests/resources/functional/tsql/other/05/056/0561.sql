--Query type: DDL
WITH DBProperties AS (SELECT 'Standard' AS Edition, 250 * 1024 AS MaxSizeMB, 'S0' AS ServiceObjective)
SELECT 'ALTER DATABASE [db1] MODIFY (EDITION = ''' + Edition + ''', MAXSIZE = ' + CONVERT(VARCHAR, MaxSizeMB) + ' MB, SERVICE_OBJECTIVE = ''' + ServiceObjective + ''');' AS Query
FROM DBProperties
