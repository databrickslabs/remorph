-- tsql sql:
CREATE TABLE #QueryStoreConfig (ConfigName sysname, ConfigValue sysname);
INSERT INTO #QueryStoreConfig (ConfigName, ConfigValue)
VALUES ('QUERY_STORE', 'ON'), ('QUERY_STORE_CAPTURE_MODE', 'ALL');
DECLARE @sql nvarchar(max) = '';
SELECT @sql += 'ALTER DATABASE SCOPED CONFIGURATION SET ' + ConfigName + ' = ''' + ConfigValue + ''';'
FROM #QueryStoreConfig;
EXEC sp_executesql @sql;
SELECT * FROM #QueryStoreConfig;
-- REMORPH CLEANUP: DROP TABLE #QueryStoreConfig;
