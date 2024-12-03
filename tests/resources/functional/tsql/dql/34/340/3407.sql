--Query type: DQL
SELECT SupplierID, CompanyName FROM (VALUES (1, 'Supplier1'), (2, 'Supplier2')) AS Suppliers (SupplierID, CompanyName) WHERE CompanyName LIKE 'Supplier%';
