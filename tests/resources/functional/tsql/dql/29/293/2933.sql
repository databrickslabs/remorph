--Query type: DQL
WITH customer_info AS (
    SELECT c_custkey, c_name, c_address
    FROM (
        VALUES (1, 'Customer1', 'Address1'),
               (2, 'Customer2', 'Address2')
    ) AS c (c_custkey, c_name, c_address)
),
order_info AS (
    SELECT o_orderkey, o_custkey, o_orderstatus
    FROM (
        VALUES (1, 1, 'O'),
               (2, 2, 'O')
    ) AS o (o_orderkey, o_custkey, o_orderstatus)
)
SELECT c.c_name, c.c_address, o.o_orderstatus
FROM customer_info AS c
JOIN order_info AS o ON c.c_custkey = o.o_custkey
WHERE NOT EXISTS (
    SELECT *
    FROM (
        VALUES ('Order1', 'Item1'),
               ('Order2', 'Item2')
    ) AS l (l_orderkey, l_partkey)
    JOIN (
        VALUES (1, 'Order1'),
               (2, 'Order2')
    ) AS ls (ls_orderkey, ls_partkey) ON l.l_orderkey = ls.ls_orderkey
    WHERE o.o_orderkey = l.l_orderkey AND l.l_partkey LIKE 'I%'
)
ORDER BY c.c_name, c.c_address
