-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-view-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
CREATE VIEW HumanResources.EmployeeHireDate  
AS  
SELECT p.FirstName, p.LastName, e.HireDate  
FROM HumanResources.Employee AS e JOIN Person.Person AS  p  
ON e.BusinessEntityID = p.BusinessEntityID ;  
GO