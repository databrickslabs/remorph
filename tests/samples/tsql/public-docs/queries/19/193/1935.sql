-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/delete-transact-sql?view=sql-server-ver16

DELETE FROM Production.ProductCostHistory  
WHERE StandardCost > 1000.00;  
GO