--Query type: DDL
SELECT SupplierName, Address INTO dbo.Supplier FROM (VALUES ('Supplier1', 'Address1'), ('Supplier2', 'Address2')) AS SupplierUSA(SupplierName, Address);
SELECT * FROM dbo.Supplier;
-- REMORPH CLEANUP: DROP TABLE dbo.Supplier;
