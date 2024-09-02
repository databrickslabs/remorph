--Query type: DDL
CREATE TABLE #app_references ( app_name sysname, table_name sysname );
INSERT INTO #app_references ( app_name, table_name )
VALUES ( 'my_new_app', 'new_table_to_read' );
DECLARE @sql nvarchar(max) = N'ALTER DATABASE [' + ( SELECT app_name FROM #app_references ) + N'] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;';
EXEC sp_executesql @sql;
SET @sql = N'ALTER DATABASE [' + ( SELECT app_name FROM #app_references ) + N'] SET MULTI_USER;';
EXEC sp_executesql @sql;
SET @sql = N'DROP TABLE [' + ( SELECT table_name FROM #app_references ) + N'];';
EXEC sp_executesql @sql;
SELECT *
FROM sys.databases
WHERE name = 'my_new_app';
-- REMORPH CLEANUP: DROP TABLE #app_references;
-- REMORPH CLEANUP: DROP DATABASE my_new_app;