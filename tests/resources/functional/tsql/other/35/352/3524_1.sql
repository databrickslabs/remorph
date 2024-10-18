--Query type: DDL
WITH SalesData AS (
    SELECT 'ProductA' AS Product, 100 AS Sales
    UNION ALL
    SELECT 'ProductB', 200
    UNION ALL
    SELECT 'ProductC', 300
)
SELECT Product, Sales
FROM SalesData;