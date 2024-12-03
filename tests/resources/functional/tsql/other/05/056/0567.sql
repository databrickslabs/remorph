--Query type: DCL
DECLARE @database_name sysname = 'db3';
DECLARE @sql nvarchar(max) = N'ALTER AVAILABILITY GROUP [YourAvailabilityGroupName] SET FAILOVER;'
EXEC sp_executesql @sql;
