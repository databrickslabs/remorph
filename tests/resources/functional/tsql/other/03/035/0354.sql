--Query type: DDL
CREATE PROCEDURE Get10TopSuppliers
AS
BEGIN
    WITH SuppliersCTE AS (
        SELECT s.SuppName, s.AnnualSales
        FROM (
            VALUES ('Supplier#000000001', 1000000.0),
                   ('Supplier#000000002', 2000000.0),
                   ('Supplier#000000003', 3000000.0),
                   ('Supplier#000000004', 4000000.0),
                   ('Supplier#000000005', 5000000.0),
                   ('Supplier#000000006', 6000000.0),
                   ('Supplier#000000007', 7000000.0),
                   ('Supplier#000000008', 8000000.0),
                   ('Supplier#000000009', 9000000.0),
                   ('Supplier#000000010', 10000000.0)
        ) AS s (SuppName, AnnualSales)
    )
    SELECT TOP (10) s.SuppName, s.AnnualSales
    FROM SuppliersCTE AS s
    ORDER BY AnnualSales DESC, SuppName ASC;
END;
-- REMORPH CLEANUP: DROP PROCEDURE Get10TopSuppliers;