USE AdventureWorks2022;
GO
SELECT SalesOrderID, ProductID, OrderQty
    ,SUM(OrderQty) OVER (PARTITION BY SalesOrderID) AS Total
    ,AVG(OrderQty) OVER (PARTITION BY SalesOrderID) AS "Avg"
    ,COUNT(OrderQty) OVER (PARTITION BY SalesOrderID) AS "Count"
    ,MIN(OrderQty) OVER (PARTITION BY SalesOrderID) AS "Min"
    ,MAX(OrderQty) OVER (PARTITION BY SalesOrderID) AS "Max"
    FROM Sales.SalesOrderDetail
WHERE SalesOrderID IN(43659,43664);
GO