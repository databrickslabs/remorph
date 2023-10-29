-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/set-rowcount-transact-sql?view=sql-server-ver16

SET ROWCOUNT 4;  
SELECT *  
FROM Production.ProductInventory  
WHERE Quantity < 300;  
GO  
  
-- (4 row(s) affected)