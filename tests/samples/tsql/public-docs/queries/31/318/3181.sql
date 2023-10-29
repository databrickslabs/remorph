-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/select-examples-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO
SELECT p1.ProductModelID
FROM Production.Product AS p1
GROUP BY p1.ProductModelID
HAVING MAX(p1.ListPrice) >= 
    (SELECT AVG(p2.ListPrice) * 2
     FROM Production.Product AS p2
     WHERE p1.ProductModelID = p2.ProductModelID);
GO