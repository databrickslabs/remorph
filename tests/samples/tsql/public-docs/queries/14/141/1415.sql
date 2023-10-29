-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-shrinkdatabase-transact-sql?view=sql-server-ver16

DBCC SHRINKDATABASE ([AdventureWorks2022], 20) WITH WAIT_AT_LOW_PRIORITY (ABORT_AFTER_WAIT = SELF);