--Query type: DML
WITH ProductCTE AS (
    SELECT ProductID, ProductName, ProductModelID, PhotoID
    FROM (
        VALUES
            (1, 'Product1', 120, 1),
            (2, 'Product2', 121, 2),
            (3, 'Product3', 122, 3),
            (4, 'Product4', 123, 4),
            (5, 'Product5', 124, 5)
    ) AS ProductTable (ProductID, ProductName, ProductModelID, PhotoID)
),
ProductModelCTE AS (
    SELECT ProductModelID, ProductModelName
    FROM (
        VALUES
            (120, 'Model1'),
            (121, 'Model2'),
            (122, 'Model3'),
            (123, 'Model4'),
            (124, 'Model5')
    ) AS ProductModelTable (ProductModelID, ProductModelName)
),
DeletedProductsCTE AS (
    SELECT p.ProductID, p.ProductName, p.ProductModelID, p.PhotoID
    FROM ProductCTE p
    INNER JOIN ProductModelCTE pm
        ON p.ProductModelID = pm.ProductModelID
    WHERE p.ProductModelID BETWEEN 120 AND 124
)
SELECT ProductID, ProductName, ProductModelID, PhotoID
FROM DeletedProductsCTE
ORDER BY ProductModelID;