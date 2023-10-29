-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/select-window-transact-sql?view=sql-server-ver16

ALTER DATABASE AdventureWorks2022 SET Compatibility_level = 160;
GO

USE AdventureWorks2022;
GO

SELECT SalesOrderID AS OrderNumber, ProductID,
    OrderQty AS Qty,
    SUM(OrderQty) OVER win AS Total,
    AVG(OrderQty) OVER(win PARTITION BY SalesOrderID) AS Avg,
    COUNT(OrderQty) OVER(win ROWS BETWEEN UNBOUNDED PRECEDING AND 1 FOLLOWING) AS Count
FROM Sales.SalesOrderDetail
WHERE SalesOrderID IN(43659,43664) AND
    ProductID LIKE '71%'
WINDOW win AS (ORDER BY SalesOrderID, ProductID);
GO