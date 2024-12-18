-- tsql sql:
CREATE TYPE SupplierInfoType AS TABLE (
    SupplierName VARCHAR(50),
    AccountBalance DECIMAL(10, 2)
);

-- REMORPH CLEANUP: DROP TYPE SupplierInfoType;
