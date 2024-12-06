-- tsql sql:
WITH CustomerCTE AS (
    SELECT c_custkey, c_name, c_address
    FROM (
        VALUES (1, 'Customer#001', '123 Main St'),
               (2, 'Customer#002', '456 Elm St')
    ) AS Customer(c_custkey, c_name, c_address)
),
OrderCTE AS (
    SELECT o_orderkey, o_custkey, o_totalprice
    FROM (
        VALUES (1, 1, 100.00),
               (2, 1, 200.00),
               (3, 2, 50.00)
    ) AS Orders(o_orderkey, o_custkey, o_totalprice)
)
SELECT c.c_name, c.c_address, o.o_totalprice, o.o_orderkey
FROM CustomerCTE c
INNER JOIN OrderCTE o ON c.c_custkey = o.o_custkey
WHERE CAST(CAST(o.o_totalprice AS INT) AS CHAR(20)) LIKE '1%';
