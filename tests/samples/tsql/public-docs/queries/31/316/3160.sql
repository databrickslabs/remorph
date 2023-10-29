-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/last-value-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO
SELECT Department
    , LastName
    , Rate
    , HireDate
    , LAST_VALUE(HireDate) OVER (
        PARTITION BY Department ORDER BY Rate
        ) AS LastValue
FROM HumanResources.vEmployeeDepartmentHistory AS edh
INNER JOIN HumanResources.EmployeePayHistory AS eph
    ON eph.BusinessEntityID = edh.BusinessEntityID
INNER JOIN HumanResources.Employee AS e
    ON e.BusinessEntityID = edh.BusinessEntityID
WHERE Department IN (N'Information Services', N'Document Control');