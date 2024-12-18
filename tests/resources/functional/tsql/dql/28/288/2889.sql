-- tsql sql:
WITH EmployeeCTE AS (
    SELECT 1 AS EmployeeID, 'John' AS EmployeeName
    UNION ALL
    SELECT 2 AS EmployeeID, 'Jane' AS EmployeeName
),
DepartmentCTE AS (
    SELECT 'Sales' AS DepartmentName
    UNION ALL
    SELECT 'Marketing' AS DepartmentName
)
SELECT e.EmployeeID, d.DepartmentName AS Department
FROM EmployeeCTE e
CROSS JOIN DepartmentCTE d
ORDER BY e.EmployeeID, d.DepartmentName;
