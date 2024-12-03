--Query type: DCL
DECLARE @login sysname = 'newlogin';
DECLARE @sql nvarchar(max) = 'CREATE LOGIN ' + QUOTENAME(@login) + ' WITH PASSWORD = ''password'';'
EXEC sp_executesql @sql;
CREATE USER [newuser] FOR LOGIN newlogin;
SELECT * FROM sys.database_principals WHERE name = 'newuser';
-- REMORPH CLEANUP: DROP USER newuser;
DROP LOGIN newlogin;
