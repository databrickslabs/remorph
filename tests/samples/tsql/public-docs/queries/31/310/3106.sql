-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/cast-and-convert-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO

SELECT p.FirstName,
    p.LastName,
    SUBSTRING(p.Title, 1, 25) AS Title,
    CAST(e.SickLeaveHours AS CHAR(1)) AS [Sick Leave]
FROM HumanResources.Employee e
INNER JOIN Person.Person p
    ON e.BusinessEntityID = p.BusinessEntityID
WHERE NOT e.BusinessEntityID > 5;
GO