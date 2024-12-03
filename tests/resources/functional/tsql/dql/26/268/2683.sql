--Query type: DQL
WITH Products AS (
    SELECT 'Road-150' AS Name, 'H' AS Class, 'Red' AS Color, 'FR-R38B-60' AS ProductNumber
    UNION ALL
    SELECT 'Road-250' AS Name, 'H' AS Class, 'Black' AS Color, 'FR-R38B-62' AS ProductNumber
    UNION ALL
    SELECT 'Mountain-100' AS Name, 'M' AS Class, 'Silver' AS Color, 'MW-M109-40' AS ProductNumber
)
SELECT Name, Class, Color, ProductNumber, COALESCE(Class, Color, ProductNumber) AS FirstNotNull
FROM Products;
