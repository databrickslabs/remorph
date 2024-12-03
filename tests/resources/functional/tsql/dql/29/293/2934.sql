--Query type: DQL
WITH ProductCTE AS (
    SELECT 'Product1' AS Name, 1 AS ProductID
    UNION ALL
    SELECT 'Product2' AS Name, 2 AS ProductID
    UNION ALL
    SELECT 'Product3' AS Name, 3 AS ProductID
),
VendorCTE AS (
    SELECT 'Vendor1' AS Name, 1 AS BusinessEntityID
    UNION ALL
    SELECT 'Vendor2' AS Name, 2 AS BusinessEntityID
    UNION ALL
    SELECT 'Vendor3' AS Name, 3 AS BusinessEntityID
),
ProductVendorCTE AS (
    SELECT 1 AS ProductID, 1 AS BusinessEntityID
    UNION ALL
    SELECT 2 AS ProductID, 2 AS BusinessEntityID
    UNION ALL
    SELECT 3 AS ProductID, 3 AS BusinessEntityID
)
SELECT p.Name AS ProductName, v.Name AS VendorName
FROM ProductCTE AS p
INNER JOIN ProductVendorCTE AS pv ON p.ProductID = pv.ProductID
INNER JOIN VendorCTE AS v ON pv.BusinessEntityID = v.BusinessEntityID
ORDER BY p.Name, v.Name;
