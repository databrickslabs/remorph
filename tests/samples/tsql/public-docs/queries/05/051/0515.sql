-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/select-window-transact-sql?view=sql-server-ver16

ALTER DATABASE AdventureWorks2022 SET Compatibility_level = 160;
GO

USE AdventureWorks2022;
GO

SELECT SalesOrderID AS OrderNumber, ProductID,
    OrderQty AS Qty,
    SUM(OrderQty) OVER win2 AS Total,
    AVG(OrderQty) OVER win1 AS Avg
FROM Sales.SalesOrderDetail
WHERE SalesOrderID IN(43659,43664) AND
    ProductID LIKE '71%'
WINDOW win1 AS (win3),
    win2 AS (ORDER BY SalesOrderID, ProductID),
    win3 AS (win2 PARTITION BY SalesOrderID);
GO