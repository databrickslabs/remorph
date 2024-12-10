-- tsql sql:
SELECT DISTINCT p.EnglishProductName
FROM (
    VALUES ('Product1', 1),
           ('Product2', 2),
           ('Product3', 3)
) AS p (EnglishProductName, ProductSubcategoryKey)
INNER JOIN (
    VALUES ('Subcategory1', 1),
           ('Subcategory2', 2),
           ('Subcategory3', 3)
) AS s (EnglishProductSubcategoryName, ProductSubcategoryKey)
    ON p.ProductSubcategoryKey = s.ProductSubcategoryKey
WHERE EXISTS (
    SELECT *
    FROM (
        VALUES ('Road Bikes', 1),
               ('Mountain Bikes', 2),
               ('Touring Bikes', 3)
    ) AS t (EnglishProductSubcategoryName, ProductSubcategoryKey)
    WHERE s.EnglishProductSubcategoryName = t.EnglishProductSubcategoryName
      AND t.EnglishProductSubcategoryName = 'Road Bikes'
)
ORDER BY p.EnglishProductName
