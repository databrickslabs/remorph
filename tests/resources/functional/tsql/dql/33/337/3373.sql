--Query type: DQL
WITH ProductCTE AS (
    SELECT ProductID, Name, Color, ListPrice
    FROM (
        VALUES
            (1, 'Product A', 'Red', 10.99),
            (2, 'Product B', 'Blue', 9.99),
            (3, 'Product C', 'Green', 12.99)
    ) AS ProductTable (ProductID, Name, Color, ListPrice)
)
SELECT ProductID, Name, Color
FROM ProductCTE
ORDER BY ListPrice;
