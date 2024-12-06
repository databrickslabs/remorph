-- tsql sql:
DECLARE @sql nvarchar(max) = 'CREATE DATABASE NewDatabase; ALTER DATABASE NewDatabase SET (AUTOGROW = ON);'; EXEC sp_executesql @sql; -- REMORPH CLEANUP: DROP DATABASE NewDatabase;
