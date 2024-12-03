--Query type: DML
TRUNCATE TABLE #Products;

WITH ProductsCTE AS (
    SELECT ProductID, ProductName
    FROM (
        VALUES (1, 'Product1'),
               (2, 'Product2')
    ) AS Products(ProductID, ProductName)
)

SELECT *
FROM ProductsCTE;
