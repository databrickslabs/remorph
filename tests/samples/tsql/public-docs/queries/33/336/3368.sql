-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/expressions-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
SELECT ProductID, 1+2  
FROM Production.Product;  
GO