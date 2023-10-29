-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/isnull-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
SELECT AVG(ISNULL(Weight, 50))  
FROM Production.Product;  
GO