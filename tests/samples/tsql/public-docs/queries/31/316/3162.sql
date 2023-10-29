-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/first-value-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO
SELECT Name, ListPrice,
       FIRST_VALUE(Name) OVER (ORDER BY ListPrice ASC) AS LeastExpensive
FROM Production.Product
WHERE ProductSubcategoryID = 37;