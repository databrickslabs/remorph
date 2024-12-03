--Query type: DDL
WITH CustomerCTE AS (
    SELECT 'Customer1' AS CustomerName, 1 AS CustomerLevel
    UNION ALL
    SELECT 'Customer2', 2
)
SELECT 0 AS [Current Level], CustomerName, CustomerLevel
FROM CustomerCTE;

SELECT 0 AS [Order Details Level];
