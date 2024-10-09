--Query type: DQL
WITH EmployeeCTE AS (
    SELECT 'John' AS EmployeeName, 10000 AS Salary, 1 AS DepartmentID
    UNION ALL
    SELECT 'Alice', 20000, 1
    UNION ALL
    SELECT 'Bob', 30000, 2
),
DepartmentCTE AS (
    SELECT 1 AS DepartmentID, 'Sales' AS DepartmentName
    UNION ALL
    SELECT 2, 'Marketing'
)
SELECT DISTINCT
    T1.DepartmentName,
    MIN(T2.Salary) OVER (PARTITION BY T1.DepartmentID) AS MinSalary,
    MAX(T2.Salary) OVER (PARTITION BY T1.DepartmentID) AS MaxSalary,
    AVG(T2.Salary) OVER (PARTITION BY T1.DepartmentID) AS AvgSalary,
    COUNT(T2.EmployeeName) OVER (PARTITION BY T1.DepartmentID) AS EmployeesPerDept
FROM
    DepartmentCTE AS T1
    JOIN EmployeeCTE AS T2 ON T1.DepartmentID = T2.DepartmentID
WHERE
    T2.Salary > 0
ORDER BY
    T1.DepartmentName;