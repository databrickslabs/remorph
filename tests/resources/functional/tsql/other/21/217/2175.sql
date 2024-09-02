--Query type: DDL
WITH TempCTE AS (
    SELECT 1 AS ID, 'Name1' AS Name
    UNION ALL
    SELECT 2 AS ID, 'Name2' AS Name
)
SELECT *
FROM TempCTE;