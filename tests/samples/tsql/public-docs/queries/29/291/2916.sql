-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-database-transact-sql-compatibility-level?view=sql-server-ver16

SELECT name, compatibility_level
FROM sys.databases
WHERE name = db_name();
GO