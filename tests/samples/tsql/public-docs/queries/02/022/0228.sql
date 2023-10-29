-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/col-name-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks  
  
SELECT COL_NAME(OBJECT_ID('dbo.FactResellerSales'), 1) AS FirstColumnName,  
COL_NAME(OBJECT_ID('dbo.FactResellerSales'), 2) AS SecondColumnName;