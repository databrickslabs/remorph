-- tsql sql:
IF OBJECT_ID('dbo.NewTable', 'U') IS NOT NULL
    DROP TABLE dbo.NewTable;

WITH CTE AS (
    SELECT 1 AS CustomerID, 'John' AS CustomerName
    UNION ALL
    SELECT 2, 'Jane'
)
SELECT CustomerID, CustomerName
INTO dbo.NewTable
FROM CTE
WHERE CustomerID IN (1, 2);

SELECT * FROM dbo.NewTable;
-- REMORPH CLEANUP: DROP TABLE dbo.NewTable;
