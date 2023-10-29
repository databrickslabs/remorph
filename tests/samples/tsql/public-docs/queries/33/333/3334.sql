-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/isnumeric-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
SELECT City, PostalCode  
FROM Person.Address   
WHERE ISNUMERIC(PostalCode) <> 1;  
GO