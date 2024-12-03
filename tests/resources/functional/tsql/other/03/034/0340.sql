--Query type: DML
WITH ProductCTE AS (
    SELECT 1 AS ProductKey, 100 AS ListPrice
    UNION ALL
    SELECT 2, 200
    UNION ALL
    SELECT 3, 300
),
UpdatedProductCTE AS (
    SELECT ProductKey, ListPrice * 2 AS NewListPrice, 0 AS Iteration
    FROM ProductCTE
    UNION ALL
    SELECT ProductKey, NewListPrice * 2, Iteration + 1
    FROM UpdatedProductCTE
    WHERE NewListPrice < 500
),
AverageCTE AS (
    SELECT AVG(NewListPrice) AS AverageNewListPrice
    FROM UpdatedProductCTE
)
SELECT *
FROM UpdatedProductCTE
WHERE NewListPrice < (SELECT AverageNewListPrice FROM AverageCTE) * 2
OPTION (MAXRECURSION 0);
