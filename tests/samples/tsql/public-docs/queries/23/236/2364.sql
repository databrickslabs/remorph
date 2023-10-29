-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-freeproccache-transact-sql?view=sql-server-ver16

SELECT * FROM sys.dm_resource_governor_resource_pools;
GO
DBCC FREEPROCCACHE ('default');
GO