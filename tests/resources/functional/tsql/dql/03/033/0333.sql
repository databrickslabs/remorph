-- tsql sql:
WITH SalesPersonCTE AS (
    SELECT 1 AS BusinessEntityID, 1000.0 AS SalesQuota, 'John' AS FirstName, 'Doe' AS LastName
),
EmployeeCTE AS (
    SELECT 1 AS BusinessEntityID
),
PersonCTE AS (
    SELECT 1 AS BusinessEntityID
)
SELECT
    sp.BusinessEntityID AS SalesPersonID,
    sp.FirstName,
    sp.LastName,
    sp.SalesQuota,
    sp.SalesQuota / 12 AS [Sales Target Per Month]
FROM
    SalesPersonCTE sp
    INNER JOIN EmployeeCTE e ON sp.BusinessEntityID = e.BusinessEntityID
    INNER JOIN PersonCTE p ON e.BusinessEntityID = p.BusinessEntityID
