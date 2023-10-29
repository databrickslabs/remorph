-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-database-transact-sql-set-options?view=sql-server-ver16

SELECT [name], user_access_desc, is_read_only FROM sys.databases
WHERE [name] = 'database_name'
GO