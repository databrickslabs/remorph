-- tsql sql:
WITH EmployeeCTE AS (
    SELECT 1 AS BusinessEntityID, 'Sales Representative' AS JobTitle
),
PurchaseOrderHeaderCTE AS (
    SELECT 1 AS EmployeeID, 1 AS VendorID
),
VendorCTE AS (
    SELECT 1 AS BusinessEntityID, 'Vendor Name' AS Name
)
SELECT e.BusinessEntityID, e.JobTitle, v.Name
FROM EmployeeCTE AS e
INNER JOIN PurchaseOrderHeaderCTE AS poh ON e.BusinessEntityID = poh.EmployeeID
INNER JOIN VendorCTE AS v ON poh.VendorID = v.BusinessEntityID
