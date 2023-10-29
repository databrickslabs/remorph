-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/cast-and-convert-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO

SELECT p.FirstName,
    p.LastName,
    s.SalesYTD,
    s.BusinessEntityID
FROM Person.Person AS p
INNER JOIN Sales.SalesPerson AS s
    ON p.BusinessEntityID = s.BusinessEntityID
WHERE CAST(CAST(s.SalesYTD AS INT) AS CHAR(20)) LIKE '2%';
GO