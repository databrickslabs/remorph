-- tsql sql:
CREATE PROCEDURE Sales.usp_SupplierAllInfo
WITH EXECUTE AS CALLER
AS
SET NOCOUNT ON;

WITH SupplierCTE AS (
    SELECT 'Supplier1' AS Name, 'Active' AS ActiveFlag, 'Good' AS CreditRating
    UNION ALL
    SELECT 'Supplier2' AS Name, 'Inactive' AS ActiveFlag, 'Fair' AS CreditRating
    UNION ALL
    SELECT 'Supplier3' AS Name, 'Active' AS ActiveFlag, 'Excellent' AS CreditRating
),
ProductCTE AS (
    SELECT 'Product1' AS Name, 'Supplier1' AS SupplierName
    UNION ALL
    SELECT 'Product2' AS Name, 'Supplier2' AS SupplierName
    UNION ALL
    SELECT 'Product3' AS Name, 'Supplier3' AS SupplierName
)

SELECT s.Name AS Supplier, p.Name AS [Product name],
       s.CreditRating AS [Rating],
       s.ActiveFlag AS Availability
FROM SupplierCTE s
INNER JOIN ProductCTE p
ON s.Name = p.SupplierName
ORDER BY s.Name ASC;

-- Execute the procedure
EXEC Sales.usp_SupplierAllInfo;

-- REMORPH CLEANUP: DROP PROCEDURE Sales.usp_SupplierAllInfo;
