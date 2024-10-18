--Query type: DQL
WITH OrderDetails AS (
    SELECT 1 AS OrderID, 10 AS ProductID, 5 AS OrderQty, '2022-01-01' AS OrderDate
),
OrderHeaders AS (
    SELECT 1 AS OrderID, '2022-01-01' AS OrderDate
)
SELECT 
    od.OrderID,
    od.ProductID,
    od.OrderQty,
    oh.OrderDate,
    DATEDIFF(day, MIN(oh.OrderDate) OVER (PARTITION BY oh.OrderID), SYSDATETIME()) AS Total
FROM 
    OrderDetails od
    INNER JOIN OrderHeaders oh ON od.OrderID = oh.OrderID
WHERE 
    oh.OrderID IN (1);