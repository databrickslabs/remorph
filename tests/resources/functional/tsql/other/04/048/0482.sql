--Query type: DDL
DECLARE @sql NVARCHAR(MAX) = N'ALTER AUTHORIZATION ON SCHEMA::dbo TO MichikoOsada';
EXEC sp_executesql @sql;
