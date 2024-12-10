-- tsql sql:
WITH Department AS (
    SELECT 'Sales' AS Name, 1 AS DepartmentID
    UNION ALL
    SELECT 'Marketing', 2
),
EmployeeDepartmentHistory AS (
    SELECT 1 AS BusinessEntityID, 1 AS DepartmentID, CAST('2020-01-01' AS DATE) AS StartDate, NULL AS EndDate
    UNION ALL
    SELECT 2, 2, '2020-01-02', NULL
),
EmployeePayHistory AS (
    SELECT 1 AS BusinessEntityID, 100.0 AS Rate
    UNION ALL
    SELECT 2, 200.0
)
SELECT DISTINCT
    d.Name AS DepartmentName,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY ph.Rate) OVER (PARTITION BY d.Name) AS MedianCont,
    PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY ph.Rate) OVER (PARTITION BY d.Name) AS MedianDisc
FROM
    Department d
    INNER JOIN EmployeeDepartmentHistory dh ON dh.DepartmentID = d.DepartmentID
    INNER JOIN EmployeePayHistory ph ON ph.BusinessEntityID = dh.BusinessEntityID
WHERE
    dh.EndDate IS NULL;
