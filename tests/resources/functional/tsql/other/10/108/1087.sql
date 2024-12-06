-- tsql sql:
CREATE PROCEDURE Sales.uspCustomerAllInfo
WITH EXECUTE AS CALLER
AS
    SET NOCOUNT ON;
    WITH CustomerCTE AS (
        SELECT c_custkey, c_name, c_address
        FROM (
            VALUES (1, 'Customer1', 'Address1'),
                   (2, 'Customer2', 'Address2'),
                   (3, 'Customer3', 'Address3')
        ) AS Customer(c_custkey, c_name, c_address)
    ),
    OrderCTE AS (
        SELECT o_orderkey, o_custkey, o_totalprice
        FROM (
            VALUES (1, 1, 100.00),
                   (2, 1, 200.00),
                   (3, 2, 300.00)
        ) AS Orders(o_orderkey, o_custkey, o_totalprice)
    )
    SELECT c.c_name AS Customer, o.o_totalprice AS 'Order Total',
      c.c_address AS 'Address'
    FROM CustomerCTE c
    INNER JOIN OrderCTE o
      ON c.c_custkey = o.o_custkey
    ORDER BY c.c_name ASC;

-- Execute the procedure
EXEC Sales.uspCustomerAllInfo;

-- REMORPH CLEANUP: DROP PROCEDURE Sales.uspCustomerAllInfo;
