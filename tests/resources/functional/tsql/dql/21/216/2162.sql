-- tsql sql:
WITH BillOfMaterialsCTE AS (
    SELECT CAST('2022-01-01' AS DATE) AS StartDate, 101 AS ComponentID
    UNION ALL
    SELECT CAST('2022-01-02' AS DATE), 202
    UNION ALL
    SELECT CAST('2022-01-03' AS DATE), 303
)
SELECT StartDate, ComponentID
FROM BillOfMaterialsCTE
WHERE ComponentID IN (101, 202, 303, 404, 505)
