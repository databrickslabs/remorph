--Query type: DQL
WITH CustomerCTE AS (
    SELECT c_custkey, c_name, c_address
    FROM (
        VALUES (1, 'Customer1', 'Address1'),
               (2, 'Customer2', 'Address2')
    ) AS c (c_custkey, c_name, c_address)
),
OrderCTE AS (
    SELECT o_orderkey, o_custkey, o_orderstatus
    FROM (
        VALUES (1, 1, 'O'),
               (2, 1, 'O')
    ) AS o (o_orderkey, o_custkey, o_orderstatus)
),
LineitemCTE AS (
    SELECT l_orderkey, l_linenumber, l_shipdate
    FROM (
        VALUES (1, 1, '1992-01-01'),
               (1, 2, '1992-01-01')
    ) AS l (l_orderkey, l_linenumber, l_shipdate)
)
SELECT RTRIM(c.c_name) + ' ' + LTRIM(c.c_address) AS CustomerName,
       o.o_orderstatus AS OrderStatus
FROM CustomerCTE c
INNER JOIN OrderCTE o ON c.c_custkey = o.o_custkey
INNER JOIN LineitemCTE l ON o.o_orderkey = l.l_orderkey
ORDER BY c.c_name, o.o_orderkey;
