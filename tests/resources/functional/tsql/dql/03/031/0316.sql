--Query type: DQL
WITH CustomerCTE AS (
    SELECT c_custkey, c_name, c_address
    FROM (
        VALUES (1, 'Customer1', 'Address1'),
               (2, 'Customer2', 'Address2')
    ) AS Customer(c_custkey, c_name, c_address)
),
OrderCTE AS (
    SELECT o_orderkey, o_custkey, o_orderstatus
    FROM (
        VALUES (1, 1, 'O'),
               (2, 1, 'O')
    ) AS Orders(o_orderkey, o_custkey, o_orderstatus)
)
SELECT c.c_name, c.c_address
FROM CustomerCTE c
INNER JOIN OrderCTE o ON c.c_custkey = o.o_custkey
WHERE EXISTS (
    SELECT *
    FROM OrderCTE o2
    WHERE o2.o_orderkey = o.o_orderkey AND o2.o_orderstatus = 'O'
)
