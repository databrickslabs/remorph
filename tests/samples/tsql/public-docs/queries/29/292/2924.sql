-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-database-transact-sql-file-and-filegroup-options?view=sql-server-ver16

SELECT name, physical_name
FROM sys.master_files
WHERE database_id = DB_ID('tempdb');
GO