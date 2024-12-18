-- tsql sql:
DECLARE @MyVariable INT = 1;

WITH EmployeeCTE AS (
    SELECT CustomerID, OrderTotal, SalesPersonID
    FROM (
        VALUES (1, 100.00, 1),
               (2, 200.00, 2),
               (3, 300.00, 1)
    ) AS EmployeeTable (CustomerID, OrderTotal, SalesPersonID)
)

SELECT CustomerID, OrderTotal, SalesPersonID
FROM EmployeeCTE
WHERE CustomerID = @MyVariable;
