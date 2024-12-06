-- tsql sql:
WITH CustomerOrders AS (
    SELECT 'C001' AS CustomerID, '2022-01-01' AS OrderDate, 100.00 AS TotalAmount, 'North' AS SalesRegion
    UNION ALL
    SELECT 'C002', '2022-01-15', 200.00, 'South'
    UNION ALL
    SELECT 'C003', '2022-02-01', 50.00, 'East'
)
SELECT *
INTO #CustomerOrders
FROM CustomerOrders;

SELECT *
FROM #CustomerOrders;

-- REMORPH CLEANUP: DROP TABLE #CustomerOrders;
