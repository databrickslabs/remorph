-- tsql sql:
WITH SalesCTE AS (
    SELECT 1 AS BusinessEntityID, 250000.01 AS SalesYTD
),
PersonCTE AS (
    SELECT 1 AS BusinessEntityID, 'Doe' AS LastName, 'John' AS FirstName
),
EmployeeSalesCTE AS (
    SELECT TOP 5 1 AS EmployeeID, 'John' AS FirstName, 'Doe' AS LastName, 250000.01 AS YearlySales
)
INSERT INTO #EmployeeSales (EmployeeID, FirstName, LastName, YearlySales)
SELECT EmployeeID, FirstName, LastName, YearlySales
FROM EmployeeSalesCTE;

SELECT inserted.EmployeeID, inserted.FirstName, inserted.LastName, inserted.YearlySales
FROM (
    SELECT TOP 1 EmployeeID, FirstName, LastName, YearlySales
    FROM #EmployeeSales
) AS inserted;

SELECT sp.BusinessEntityID, p.LastName, p.FirstName, sp.SalesYTD
FROM SalesCTE sp
INNER JOIN PersonCTE p ON sp.BusinessEntityID = p.BusinessEntityID
WHERE sp.SalesYTD > 250000.00
ORDER BY sp.SalesYTD DESC;

SELECT * FROM #EmployeeSales;
