-- tsql sql:
WITH CustomerCTE AS (
    SELECT c_custkey, c_name, c_address
    FROM (
        VALUES (1, 'Customer1', 'Address1'),
               (2, 'Customer2', 'Address2')
    ) AS c (c_custkey, c_name, c_address)
),
OrderCTE AS (
    SELECT o_orderkey, o_custkey, o_totalprice
    FROM (
        VALUES (1, 1, 100.0),
               (2, 1, 200.0),
               (3, 2, 50.0)
    ) AS o (o_orderkey, o_custkey, o_totalprice)
)
SELECT c.c_custkey, c.c_name, c.c_address
FROM CustomerCTE c
GROUP BY c.c_custkey, c.c_name, c.c_address
HAVING 5000 <= (
    SELECT SUM(o.o_totalprice)
    FROM OrderCTE o
    WHERE c.c_custkey = o.o_custkey
)
ORDER BY c.c_custkey;
