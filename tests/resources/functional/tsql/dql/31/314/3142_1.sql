--Query type: DQL
WITH CustomerCTE AS (
    SELECT 'Smith' AS LastName, 'John' AS FirstName, 'Sales' AS JobTitle
),
EmployeeCTE AS (
    SELECT 'Johnson' AS LastName, 'Mike' AS FirstName, 'Marketing' AS JobTitle
)
SELECT c.LastName, c.FirstName, e.JobTitle
INTO #CustomerEmployee
FROM CustomerCTE c
JOIN EmployeeCTE e ON e.LastName = c.LastName
WHERE c.LastName = 'Smith';
