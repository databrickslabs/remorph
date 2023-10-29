-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/avg-transact-sql?view=sql-server-ver16

SELECT AVG(DISTINCT ListPrice)  
FROM Production.Product;