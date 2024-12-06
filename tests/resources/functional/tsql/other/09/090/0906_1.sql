-- tsql sql:
WITH EmployeeData AS (
    SELECT *
    FROM (
        VALUES
            (1, 'John', 'Doe'),
            (2, 'Jane', 'Doe')
    ) AS EmployeeData (EmpId, FirstName, LastName)
)
SELECT *
FROM EmployeeData
WHERE EmpId = 1;
