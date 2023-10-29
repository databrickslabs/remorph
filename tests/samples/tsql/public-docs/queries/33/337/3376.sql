-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/space-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;  
GO  
SELECT RTRIM(LastName) + ',' + SPACE(2) +  LTRIM(FirstName)  
FROM Person.Person  
ORDER BY LastName, FirstName;  
GO