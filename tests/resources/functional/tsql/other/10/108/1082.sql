-- tsql sql:
CREATE PROCEDURE Sales.uspEncryptCustomer
WITH ENCRYPTION
AS
    SET NOCOUNT ON;
    WITH CustomerCTE AS (
        SELECT c_custkey, c_name, c_address, c_phone, c_acctbal
        FROM (
            VALUES (1, 'Customer#001', '123 Main St', '123-456-7890', 100.00),
                   (2, 'Customer#002', '456 Elm St', '987-654-3210', 200.00),
                   (3, 'Customer#003', '789 Oak St', '555-123-4567', 300.00)
        ) AS Customer (c_custkey, c_name, c_address, c_phone, c_acctbal)
    )
    SELECT c_custkey, c_name, c_address, c_phone, c_acctbal
    FROM CustomerCTE;

-- Execute the procedure to test it
EXECUTE Sales.uspEncryptCustomer;

-- REMORPH CLEANUP: DROP PROCEDURE Sales.uspEncryptCustomer;
