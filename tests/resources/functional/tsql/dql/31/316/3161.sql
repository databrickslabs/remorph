--Query type: DQL
WITH EmployeeCTE AS (
    SELECT 'Sales Representative' AS JobTitle, 'Smith' AS LastName, 10 AS VacationHours, 1 AS BusinessEntityID
    UNION ALL
    SELECT 'Sales Representative', 'Johnson', 20, 2
    UNION ALL
    SELECT 'Sales Manager', 'Williams', 30, 3
),
PersonCTE AS (
    SELECT 'Smith' AS LastName, 1 AS BusinessEntityID
    UNION ALL
    SELECT 'Johnson', 2
    UNION ALL
    SELECT 'Williams', 3
)
SELECT e.JobTitle, e.LastName, e.VacationHours, FIRST_VALUE(e.LastName) OVER (PARTITION BY e.JobTitle ORDER BY e.VacationHours ASC ROWS UNBOUNDED PRECEDING) AS FewestVacationHours
FROM EmployeeCTE AS e
INNER JOIN PersonCTE AS p ON e.BusinessEntityID = p.BusinessEntityID
ORDER BY e.JobTitle;