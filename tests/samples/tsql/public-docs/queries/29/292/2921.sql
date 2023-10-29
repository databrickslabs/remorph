-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-database-transact-sql-set-options?view=sql-server-ver16

SELECT name, is_result_set_caching_on FROM sys.databases
WHERE name = <'Your_Database_Name'>