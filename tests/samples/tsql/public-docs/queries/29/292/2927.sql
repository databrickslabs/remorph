-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-statistics-transact-sql?view=sql-server-ver16

SELECT object_id, [name], auto_drop
FROM sys.stats;