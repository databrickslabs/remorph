-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-freesystemcache-transact-sql?view=sql-server-ver16

-- Clean all the caches with entries specific to the
-- resource pool named "default".
DBCC FREESYSTEMCACHE ('ALL', [default]);