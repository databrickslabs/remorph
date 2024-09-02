--Query type: DDL
DROP TABLE #TempTable;

WITH TempData AS (
    SELECT 1 AS ID, 'John' AS Name
    UNION ALL
    SELECT 2, 'Alice'
)

SELECT ID, Name
FROM TempData;