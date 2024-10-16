--Query type: DQL
WITH EmployeeCTE AS (
    SELECT 'Sales Manager' AS JobTitle, 'John' AS Name, 1 AS BusinessEntityID
    UNION ALL
    SELECT 'Sales Representative', 'Alice', 2
),
DepartmentCTE AS (
    SELECT 'Sales' AS Name, 12 AS DepartmentID
    UNION ALL
    SELECT 'Marketing', 14
),
EmployeeDepartmentHistoryCTE AS (
    SELECT 1 AS BusinessEntityID, 12 AS DepartmentID, NULL AS EndDate
    UNION ALL
    SELECT 2, 14, NULL
)
SELECT
    D.Name,
    CASE
        WHEN GROUPING_ID(D.Name, E.JobTitle) = 0 THEN E.JobTitle
        WHEN GROUPING_ID(D.Name, E.JobTitle) = 1 THEN 'Total: ' + D.Name
        WHEN GROUPING_ID(D.Name, E.JobTitle) = 3 THEN 'Company Total:'
        ELSE 'Unknown'
    END AS 'Job Title',
    COUNT(E.BusinessEntityID) AS 'Employee Count'
FROM
    EmployeeCTE E
    INNER JOIN EmployeeDepartmentHistoryCTE DH ON E.BusinessEntityID = DH.BusinessEntityID
    INNER JOIN DepartmentCTE D ON D.DepartmentID = DH.DepartmentID
WHERE
    DH.EndDate IS NULL
    AND D.DepartmentID IN (12, 14)
GROUP BY
    ROLLUP(D.Name, E.JobTitle)