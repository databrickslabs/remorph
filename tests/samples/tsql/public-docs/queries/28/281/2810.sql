-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/newid-transact-sql?view=sql-server-ver16

SELECT TOP 1 ProductID, Name, ProductNumber
FROM Production.Product
ORDER BY NEWID()
GO