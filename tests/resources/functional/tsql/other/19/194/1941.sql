--Query type: DML
WITH TempResult AS (
    SELECT 1 AS CustomerKey, 'John' AS CustomerName, 100.00 AS OrderTotal
    UNION ALL
    SELECT 2, 'Jane', 200.00
    UNION ALL
    SELECT 3, 'Bob', 300.00
)
SELECT *
FROM TempResult
WHERE OrderTotal > 200.00;
