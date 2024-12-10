-- tsql sql:
DECLARE @NewName nvarchar(50) = 'NewName';
CREATE ROLE NewRole;
DROP ROLE NewRole;
DECLARE @sql nvarchar(max) = 'CREATE ROLE ' + QUOTENAME(@NewName);
EXEC sp_executesql @sql;
-- REMORPH CLEANUP: DROP ROLE NewName;
SELECT * FROM sys.database_principals WHERE name = @NewName;
