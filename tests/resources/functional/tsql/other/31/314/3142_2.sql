--Query type: DDL
IF OBJECT_ID('dbo.DepartmentThree', 'U') IS NOT NULL
DROP TABLE dbo.DepartmentThree;

WITH DepartmentCTE AS (
    SELECT 'Sales' AS DepartmentName, 100 AS DepartmentID
    UNION ALL
    SELECT 'Marketing', 200
)
SELECT * FROM DepartmentCTE;

-- REMORPH CLEANUP: DROP TABLE dbo.DepartmentThree;