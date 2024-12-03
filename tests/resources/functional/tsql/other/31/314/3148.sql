--Query type: DCL
SELECT TOP 10 *
FROM (
    VALUES
        (1, 'John', 'Doe'),
        (2, 'Jane', 'Doe')
) AS Employees (
    Id,
    FirstName,
    LastName
)
ORDER BY Id DESC;
