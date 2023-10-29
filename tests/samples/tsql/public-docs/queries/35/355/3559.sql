-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/isnumeric-transact-sql?view=sql-server-ver16

USE master;  
GO  
SELECT name, ISNUMERIC(name) AS IsNameANumber, database_id, ISNUMERIC(database_id) AS IsIdANumber   
FROM sys.databases;  
GO