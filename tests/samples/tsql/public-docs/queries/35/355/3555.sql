-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/db-name-transact-sql?view=sql-server-ver16

USE master;  
GO  
SELECT DB_NAME(3) AS [Database Name];  
GO