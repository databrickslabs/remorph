-- tsql sql:
DECLARE @AsOfFrom DATETIME2 = DATEADD(month, -12, SYSUTCDATETIME());
DECLARE @AsOfTo DATETIME2 = DATEADD(month, -6, SYSUTCDATETIME());

WITH DEPARTMENT_CTE AS (
    SELECT 10 AS DepartmentNumber, 'Sales' AS DepartmentName, 101 AS ManagerID, 1 AS ParentDepartmentNumber
    UNION ALL
    SELECT 20 AS DepartmentNumber, 'Marketing' AS DepartmentName, 102 AS ManagerID, 1 AS ParentDepartmentNumber
    UNION ALL
    SELECT 30 AS DepartmentNumber, 'IT' AS DepartmentName, 103 AS ManagerID, 1 AS ParentDepartmentNumber
)
SELECT DepartmentNumber,
    DepartmentName,
    ManagerID,
    ParentDepartmentNumber
FROM DEPARTMENT_CTE
WHERE ManagerID = 101;
