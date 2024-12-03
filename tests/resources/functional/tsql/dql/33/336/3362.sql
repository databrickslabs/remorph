--Query type: DQL
WITH Products AS (
    SELECT 'Product1' AS Name, 5.00 AS Weight, 'Red' AS Color
    UNION ALL
    SELECT 'Product2', 15.00, 'Blue'
    UNION ALL
    SELECT 'Product3', 8.00, NULL
)
SELECT Name, Weight, Color
FROM Products
WHERE Weight < 10.00 OR Color IS NULL
ORDER BY Name;
