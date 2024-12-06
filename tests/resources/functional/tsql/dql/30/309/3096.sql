-- tsql sql:
WITH temp_result AS (
    SELECT 'P1' AS ProductNumber, 'Product 1' AS Name, 10.0 AS ListPrice
    UNION ALL
    SELECT 'P2', 'Product 2', 200.0
    UNION ALL
    SELECT 'P3', 'Product 3', 1500.0
)
SELECT
    ProductNumber,
    Name,
    "Price Range" = CASE
        WHEN ListPrice = 0 THEN 'Mfg item - not for resale'
        WHEN ListPrice < 50 THEN 'Under $50'
        WHEN ListPrice >= 50 AND ListPrice < 250 THEN 'Under $250'
        WHEN ListPrice >= 250 AND ListPrice < 1000 THEN 'Under $1000'
        ELSE 'Over $1000'
    END
FROM temp_result
ORDER BY ProductNumber
