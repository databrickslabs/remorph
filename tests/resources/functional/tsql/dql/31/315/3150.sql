--Query type: DQL
WITH Products AS (
    SELECT 'Product1' AS Name, 10.99 AS Price
    UNION ALL
    SELECT 'Product2' AS Name, 9.99 AS Price
    UNION ALL
    SELECT 'Product3' AS Name, 12.99 AS Price
)
SELECT *
FROM Products
ORDER BY Name ASC;
