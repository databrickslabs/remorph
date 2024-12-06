-- tsql sql:
WITH ProductsCTE AS (
    SELECT ProductID, ListPrice
    FROM (
        VALUES (1, 30.0),
               (2, 50.0),
               (3, 75.0),
               (4, 90.0),
               (5, 110.0)
    ) AS Products(ProductID, ListPrice)
)
SELECT *
INTO #NewProducts
FROM ProductsCTE
WHERE ListPrice > 25 AND ListPrice < 100;

SELECT *
FROM #NewProducts;

-- REMORPH CLEANUP: DROP TABLE #NewProducts;
