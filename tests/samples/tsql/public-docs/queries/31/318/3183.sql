-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/set-nocount-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO
SET NOCOUNT OFF;
GO
-- Display the count message.
SELECT TOP(5) LastName
FROM Person.Person
WHERE LastName LIKE 'A%';
GO
-- SET NOCOUNT to ON to no longer display the count message.
SET NOCOUNT ON;
GO
SELECT TOP(5) LastName
FROM Person.Person
WHERE LastName LIKE 'A%';
GO
-- Reset SET NOCOUNT to OFF
SET NOCOUNT OFF;
GO