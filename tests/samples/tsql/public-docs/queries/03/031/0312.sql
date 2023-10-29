-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/modulo-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks  
  
SELECT TOP(100)ProductID, UnitPrice, OrderQty,  
   CAST((UnitPrice) AS INT) % OrderQty AS Modulo  
FROM Sales.SalesOrderDetail;  
GO