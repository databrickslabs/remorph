--Query type: DQL
WITH ProductModelCTE AS (
    SELECT 1 AS ProductModelID, 'Model1' AS Name
    UNION ALL
    SELECT 2, 'Model2'
    UNION ALL
    SELECT 5, 'Model5'
),
GlovesCTE AS (
    SELECT 1 AS ProductModelID, 'Gloves1' AS Name
    UNION ALL
    SELECT 2, 'Gloves2'
)
SELECT ProductModelID, Name
FROM ProductModelCTE
WHERE ProductModelID NOT IN (3, 4)
UNION
SELECT ProductModelID, Name
FROM GlovesCTE
ORDER BY Name;