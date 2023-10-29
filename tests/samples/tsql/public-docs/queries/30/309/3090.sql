-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/output-clause-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO

IF OBJECT_ID('dbo.EmployeeSales', 'U') IS NOT NULL
    DROP TABLE dbo.EmployeeSales;
GO

CREATE TABLE dbo.EmployeeSales (
    EmployeeID INT IDENTITY(1, 5) NOT NULL,
    LastName NVARCHAR(20) NOT NULL,
    FirstName NVARCHAR(20) NOT NULL,
    CurrentSales MONEY NOT NULL,
    ProjectedSales AS CurrentSales * 1.10
);
GO

DECLARE @MyTableVar TABLE (
    EmployeeID INT NOT NULL,
    LastName NVARCHAR(20) NOT NULL,
    FirstName NVARCHAR(20) NOT NULL,
    CurrentSales MONEY NOT NULL,
    ProjectedSales MONEY NOT NULL
);

INSERT INTO dbo.EmployeeSales (
    LastName,
    FirstName,
    CurrentSales
)
OUTPUT INSERTED.EmployeeID,
    INSERTED.LastName,
    INSERTED.FirstName,
    INSERTED.CurrentSales,
    INSERTED.ProjectedSales
INTO @MyTableVar
SELECT c.LastName,
    c.FirstName,
    sp.SalesYTD
FROM Sales.SalesPerson AS sp
INNER JOIN Person.Person AS c
    ON sp.BusinessEntityID = c.BusinessEntityID
WHERE sp.BusinessEntityID LIKE '2%'
ORDER BY c.LastName,
    c.FirstName;

SELECT EmployeeID,
    LastName,
    FirstName,
    CurrentSales,
    ProjectedSales
FROM @MyTableVar;
GO

SELECT EmployeeID,
    LastName,
    FirstName,
    CurrentSales,
    ProjectedSales
FROM dbo.EmployeeSales;
GO