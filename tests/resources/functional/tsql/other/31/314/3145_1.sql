-- tsql sql:
WITH ProductCTE AS (
    SELECT 1 AS ProductModelID, 'Model1' AS Name
    UNION
    SELECT 2, 'Model2'
    UNION
    SELECT 5, 'Model5'
),
GlovesCTE AS (
    SELECT 1 AS ProductModelID, 'Gloves1' AS Name
    UNION
    SELECT 6, 'Gloves6'
)
SELECT ProductModelID, Name
INTO ProductResults
FROM (
    SELECT ProductModelID, Name
    FROM ProductCTE
    WHERE ProductModelID NOT IN (3, 4)
    UNION
    SELECT ProductModelID, Name
    FROM GlovesCTE
) AS DerivedTable;
