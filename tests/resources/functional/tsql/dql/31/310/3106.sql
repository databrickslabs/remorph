--Query type: DQL
WITH EmployeeCTE AS (
    SELECT 1 AS EmployeeID, 'John' AS FirstName, 'Doe' AS LastName, 8 AS SickLeaveHours
),
PersonCTE AS (
    SELECT 1 AS BusinessEntityID, 'Mr.' AS Title
)
SELECT
    e.FirstName,
    e.LastName,
    SUBSTRING(p.Title, 1, 25) AS Title,
    CAST(e.SickLeaveHours AS CHAR(1)) AS [Sick Leave]
FROM
    EmployeeCTE e
    INNER JOIN PersonCTE p ON e.EmployeeID = p.BusinessEntityID
WHERE
    NOT e.EmployeeID > 5
