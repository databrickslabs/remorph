-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-freeproccache-transact-sql?view=sql-server-ver16

-- Remove the specific plan from the cache.
DBCC FREEPROCCACHE (0x060006001ECA270EC0215D05000000000000000000000000);
GO