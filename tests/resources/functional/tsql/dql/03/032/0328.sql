-- tsql sql:
WITH CustomerCTE AS (
    SELECT c_custkey, c_name, c_address
    FROM (
        VALUES (1, 'Customer1', 'Address1'),
               (2, 'Customer2', 'Address2')
    ) AS Customer(c_custkey, c_name, c_address)
),
OrderCTE AS (
    SELECT o_orderkey, o_custkey, o_totalprice
    FROM (
        VALUES (1, 1, 100.0),
               (2, 1, 200.0)
    ) AS Orders(o_orderkey, o_custkey, o_totalprice)
)
SELECT c.c_name, c.c_address, o.o_totalprice, c.c_custkey + o.o_orderkey AS [Total Key]
FROM CustomerCTE AS c
JOIN OrderCTE AS o ON c.c_custkey = o.o_custkey
ORDER BY c.c_custkey + o.o_orderkey ASC;
