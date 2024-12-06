-- tsql sql:
WITH temp_result AS (
    SELECT 'Product1' AS ProductName, 33.99 AS ListPrice
    UNION ALL
    SELECT 'Product2', 33.49
    UNION ALL
    SELECT 'Product3', 32.99
)
SELECT SUBSTRING(ProductName, 1, 30) AS ProductName, ListPrice
FROM temp_result
WHERE CONVERT(INT, ListPrice) LIKE '33%';
