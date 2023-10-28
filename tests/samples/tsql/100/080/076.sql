USE AdventureWorks2022;
GO

SELECT SalesOrderID AS OrderNumber, ProductID,
    OrderQty AS Qty,
    SUM(OrderQty) OVER (ORDER BY SalesOrderID, ProductID) AS Total,
    AVG(OrderQty) OVER(PARTITION BY SalesOrderID ORDER BY SalesOrderID, ProductID) AS Avg,
    COUNT(OrderQty) OVER(ORDER BY SalesOrderID, ProductID ROWS BETWEEN UNBOUNDED PRECEDING AND 1 FOLLOWING) AS Count
FROM Sales.SalesOrderDetail
WHERE SalesOrderID IN(43659,43664) AND
    ProductID LIKE '71%';
GO