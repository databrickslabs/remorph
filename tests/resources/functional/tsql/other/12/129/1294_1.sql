-- tsql sql:
WITH TempCustomer AS (
    SELECT 'Customer1' AS CustomerName, 1 AS CustomerID
    UNION ALL
    SELECT 'Customer2' AS CustomerName, 2 AS CustomerID
),
TempCustomer_upsert AS (
    SELECT 'Customer3' AS CustomerName, 3 AS CustomerID
    UNION ALL
    SELECT 'Customer4' AS CustomerName, 4 AS CustomerID
)
SELECT *
FROM TempCustomer
UNION ALL
SELECT *
FROM TempCustomer_upsert;
