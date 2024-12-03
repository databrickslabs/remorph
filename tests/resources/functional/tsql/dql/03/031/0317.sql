--Query type: DQL
WITH CustomerCTE AS (
    SELECT 'John' AS FirstName, 'Smith' AS LastName, 1 AS CustomerID
    UNION ALL
    SELECT 'Jane', 'Doe', 2
),
EmployeeCTE AS (
    SELECT 'John' AS FirstName, 'Smith' AS LastName, 1 AS EmployeeID
    UNION ALL
    SELECT 'Jane', 'Doe', 2
)
SELECT c.FirstName, c.LastName
FROM CustomerCTE c
WHERE c.LastName IN (
    SELECT e.LastName
    FROM EmployeeCTE e
    WHERE c.CustomerID = e.EmployeeID AND e.LastName = 'Smith'
)
