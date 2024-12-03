--Query type: DDL
DECLARE @SchemaName sysname = 'SalesSchema';
DECLARE @NewOwner sysname = 'SalesUser';
DECLARE @sql nvarchar(max) = N'ALTER AUTHORIZATION ON SCHEMA::' + QUOTENAME(@SchemaName) + ' TO ' + QUOTENAME(@NewOwner) + ';'
EXEC sp_executesql @sql;
SELECT s.name AS SchemaName, s.principal_id AS OwnerID
FROM sys.schemas s
WHERE s.name = @SchemaName;
