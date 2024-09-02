--Query type: DML
DECLARE @v INT;

WITH EmployeeCTE AS (
    SELECT BusinessEntityID
    FROM (
        VALUES (1), (2), (3)
    ) AS Employee(BusinessEntityID)
),
EmployeeAddressCTE AS (
    SELECT BusinessEntityID
    FROM (
        VALUES (1), (2), (3)
    ) AS EmployeeAddress(BusinessEntityID)
),
CombinedCTE AS (
    SELECT BusinessEntityID
    FROM EmployeeCTE
    UNION ALL
    SELECT BusinessEntityID
    FROM EmployeeAddressCTE
)

SELECT TOP 1 @v = BusinessEntityID
FROM CombinedCTE;

SELECT @v;