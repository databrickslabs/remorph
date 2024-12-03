--Query type: DQL
WITH SupplierCTE AS (
    SELECT 'Supplier1' AS SupplierName, 1 AS SupplierID
    UNION ALL
    SELECT 'Supplier2', 2
)
SELECT SCHEMA_ID('sales') AS SalesSchemaID, SupplierName, SupplierID
FROM SupplierCTE;
