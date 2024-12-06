-- tsql sql:
WITH DepartmentCTE AS (
    SELECT 1 AS DepartmentNumber, 'Sales' AS DepartmentName, 5 AS ManagerID, 0 AS ParentDepartmentNumber
    UNION ALL
    SELECT 2 AS DepartmentNumber, 'Marketing' AS DepartmentName, 6 AS ManagerID, 1 AS ParentDepartmentNumber
)
SELECT DepartmentNumber, DepartmentName, ManagerID, ParentDepartmentNumber
FROM DepartmentCTE
WHERE ManagerID = 5;
