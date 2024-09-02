--Query type: DQL
WITH ProductModelCTE AS (
    SELECT ProductModelID, Name
    FROM (
        VALUES (1, 'Model1'),
               (2, 'Model2'),
               (5, 'Model5')
    ) AS ProductModel(ProductModelID, Name)
),
GlovesCTE AS (
    SELECT ProductModelID, Name
    FROM (
        VALUES (1, 'Gloves1'),
               (2, 'Gloves2')
    ) AS Gloves(ProductModelID, Name)
)
SELECT ProductModelID, Name
FROM ProductModelCTE
WHERE ProductModelID NOT IN (3, 4)
UNION
SELECT ProductModelID, Name
FROM GlovesCTE;