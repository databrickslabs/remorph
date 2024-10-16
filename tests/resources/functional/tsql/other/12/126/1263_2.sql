--Query type: DML
CREATE TABLE #EmployeeSales
(
    BusinessEntityID INT,
    LastName VARCHAR(50),
    SalesYTD DECIMAL(10, 2)
);

WITH SalesPerson AS
(
    SELECT 1 AS BusinessEntityID, 'Smith' AS LastName, 1000.00 AS SalesYTD
    UNION ALL
    SELECT 2 AS BusinessEntityID, 'Johnson' AS LastName, 2000.00 AS SalesYTD
    UNION ALL
    SELECT 3 AS BusinessEntityID, 'Williams' AS LastName, 3000.00 AS SalesYTD
),
Customer AS
(
    SELECT 1 AS BusinessEntityID, 'Smith' AS LastName
    UNION ALL
    SELECT 2 AS BusinessEntityID, 'Johnson' AS LastName
    UNION ALL
    SELECT 3 AS BusinessEntityID, 'Williams' AS LastName
)
INSERT INTO #EmployeeSales
SELECT sp.BusinessEntityID, c.LastName, sp.SalesYTD
FROM SalesPerson sp
INNER JOIN Customer c ON sp.BusinessEntityID = c.BusinessEntityID
WHERE sp.BusinessEntityID LIKE '2%'
ORDER BY sp.BusinessEntityID, c.LastName;

SELECT * FROM #EmployeeSales;
-- REMORPH CLEANUP: DROP TABLE #EmployeeSales;