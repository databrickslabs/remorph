-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/max-transact-sql?view=sql-server-ver16

SELECT MAX(name) FROM sys.databases WHERE database_id < 5;