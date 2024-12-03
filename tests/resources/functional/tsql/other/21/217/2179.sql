--Query type: DDL
CREATE PROCEDURE dbo.uspCustomerByOrder
AS
BEGIN
    WITH CustomerCTE AS (
        SELECT c_custkey, c_name, c_address
        FROM (
            VALUES (1, 'Customer#001', '123 Main St'),
                   (2, 'Customer#002', '456 Elm St'),
                   (3, 'Customer#003', '789 Oak St')
        ) AS Customer (c_custkey, c_name, c_address)
    ),
    OrderCTE AS (
        SELECT o_orderkey, o_custkey, o_orderstatus
        FROM (
            VALUES (1, 1, 'O'),
                   (2, 1, 'O'),
                   (3, 2, 'O')
        ) AS Orders (o_orderkey, o_custkey, o_orderstatus)
    )
    SELECT c.c_custkey, c.c_name, c.c_address, o.o_orderkey, o.o_orderstatus
    FROM CustomerCTE c
    INNER JOIN OrderCTE o ON c.c_custkey = o.o_custkey;
END;
EXECUTE dbo.uspCustomerByOrder;
-- REMORPH CLEANUP: DROP PROCEDURE dbo.uspCustomerByOrder;
