-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/count-transact-sql?view=sql-server-ver16

USE ssawPDW;
  
SELECT COUNT(*)
FROM dbo.DimEmployee;