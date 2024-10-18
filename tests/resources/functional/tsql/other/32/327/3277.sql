--Query type: DML
WITH TempCTE AS (
    SELECT 1 AS ID, 'John' AS Name
    UNION ALL
    SELECT 2 AS ID, 'Doe' AS Name
)
SELECT 'Hello, World.' AS Message, *
FROM TempCTE;