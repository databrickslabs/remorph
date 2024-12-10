-- tsql sql:
WITH Data AS (
    SELECT 'Product 1' AS ProductName, 100.0 AS Price
    UNION ALL
    SELECT 'Product 2', 200.0
    UNION ALL
    SELECT 'Product 3', 300.0
)
SELECT ProductName, Price
FROM Data;
