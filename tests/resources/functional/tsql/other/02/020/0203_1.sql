-- tsql sql:
BEGIN TRANSACTION;
SELECT *
FROM (
    VALUES (
        1, 'John', 'Doe'
        , (2, 'Jane', 'Doe')
    )
) AS Employees (
    Id
    , FirstName
    , LastName
)
WHERE Id = 1
