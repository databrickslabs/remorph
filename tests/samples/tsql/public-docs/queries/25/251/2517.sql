-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-clonedatabase-transact-sql?view=sql-server-ver16

SELECT DATABASEPROPERTYEX('clone_database_name', 'IsVerifiedClone');