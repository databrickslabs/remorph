--Query type: DDL
CREATE TABLE supplier (supplier_key INT, credit_limit DECIMAL(10, 2));
CREATE INDEX FISupplierWithCreditLimit ON supplier (supplier_key, credit_limit);
IF EXISTS (SELECT name FROM sys.indexes WHERE name = N'FISupplierWithCreditLimit' AND object_id = OBJECT_ID(N'supplier'))
    DROP INDEX FISupplierWithCreditLimit ON supplier;
SELECT * FROM supplier;
-- REMORPH CLEANUP: DROP TABLE supplier;