-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/multiply-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks  
  
SELECT ProductID, Name, ListPrice, ListPrice * 1.15 AS NewPrice  
FROM Production.Product  
WHERE Name LIKE 'Mountain-%'  
ORDER BY ProductID ASC;  
GO