-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-freesystemcache-transact-sql?view=sql-server-ver16

DBCC FREESYSTEMCACHE ('ALL') WITH MARK_IN_USE_FOR_REMOVAL;