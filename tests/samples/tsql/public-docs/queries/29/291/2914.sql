-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/reverse-transact-sql?view=sql-server-ver16

SELECT name, REVERSE(name) FROM sys.databases;  
GO