--Query type: DQL
WITH EmployeeCTE AS (
    SELECT 'DataSource1' AS DataSource, 1 AS BusinessEntityID, 'Smith' AS LastName, 1000.00 AS SalesDollars
    UNION ALL
    SELECT 'DataSource2', 2, 'Johnson', 2000.00
)
SELECT DataSource, BusinessEntityID, LastName, SalesDollars
FROM EmployeeCTE
