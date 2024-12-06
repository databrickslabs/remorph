-- tsql sql:
WITH SalesOrderDetail AS (
    SELECT 1 AS ProductID, 10.99 AS UnitPrice, 2 AS OrderQty
    UNION ALL
    SELECT 2 AS ProductID, 5.99 AS UnitPrice, 3 AS OrderQty
    UNION ALL
    SELECT 3 AS ProductID, 7.99 AS UnitPrice, 1 AS OrderQty
)
SELECT TOP (100) ProductID, UnitPrice, OrderQty, CAST(UnitPrice AS INT) % OrderQty AS Modulo
FROM SalesOrderDetail;
