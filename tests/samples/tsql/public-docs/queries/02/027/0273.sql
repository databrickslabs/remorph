-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/left-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks  
  
SELECT LEFT(EnglishProductName, 5)   
FROM dbo.DimProduct  
ORDER BY ProductKey;