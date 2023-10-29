-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/subtract-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks  
  
SELECT MAX(BaseRate) - MIN(BaseRate) AS BaseRateDifference  
FROM DimEmployee;