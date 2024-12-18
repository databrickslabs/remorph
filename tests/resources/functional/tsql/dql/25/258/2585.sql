-- tsql sql:
WITH DepartmentCTE AS (
    SELECT 1 AS DepartmentNumber, 'Sales' AS DepartmentName, 5 AS ManagerID, 0 AS ParentDepartmentNumber, '2013-01-01' AS ValidFrom, '2014-01-01' AS ValidTo
    UNION ALL
    SELECT 2 AS DepartmentNumber, 'Marketing' AS DepartmentName, 6 AS ManagerID, 1 AS ParentDepartmentNumber, '2013-01-01' AS ValidFrom, '2014-01-01' AS ValidTo
)
SELECT DepartmentNumber, DepartmentName, ManagerID, ParentDepartmentNumber
FROM DepartmentCTE
WHERE ValidFrom <= '2014-01-01' AND ValidTo > '2013-01-01' AND ManagerID = 5;
