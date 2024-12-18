-- tsql sql:
WITH EmployeeList AS (
    SELECT 1 AS Id, 'John' AS FirstName, 'Doe' AS LastName
    UNION ALL
    SELECT 2, 'Jane', 'Doe'
)
SELECT *
FROM EmployeeList
WHERE Id = 1;
