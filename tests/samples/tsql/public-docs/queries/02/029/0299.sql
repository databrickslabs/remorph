-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/space-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks  
  
SELECT RTRIM(LastName) + ',' + SPACE(2) +  LTRIM(FirstName)  
FROM dbo.DimCustomer  
ORDER BY LastName, FirstName;  
GO