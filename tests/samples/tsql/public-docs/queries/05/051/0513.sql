-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/select-window-transact-sql?view=sql-server-ver16

ALTER DATABASE AdventureWorks2022 SET Compatibility_level = 160;
GO

USE AdventureWorks2022;
GO

SELECT ROW_NUMBER() OVER win AS "Row Number",
    p.LastName, s.SalesYTD, a.PostalCode
FROM Sales.SalesPerson AS s
    INNER JOIN Person.Person AS p
        ON s.BusinessEntityID = p.BusinessEntityID
    INNER JOIN Person.Address AS a
        ON a.AddressID = p.BusinessEntityID
WHERE TerritoryID IS NOT NULL
    AND SalesYTD <> 0
WINDOW win AS (PARTITION BY PostalCode ORDER BY SalesYTD DESC)
ORDER BY PostalCode;
GO