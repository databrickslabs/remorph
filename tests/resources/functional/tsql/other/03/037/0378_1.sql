-- tsql sql:
WITH ProductDim AS (
    SELECT 1 AS ProductKey, 'Product1' AS ProductName
    UNION ALL
    SELECT 2, 'Product2'
)
SELECT *
FROM ProductDim;
