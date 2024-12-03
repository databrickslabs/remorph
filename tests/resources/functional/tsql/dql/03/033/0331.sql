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
),
LineitemCTE AS (
    SELECT l_orderkey, l_extendedprice, l_discount
    FROM (
        VALUES (1, 10.0, 0.1),
               (2, 20.0, 0.2)
    ) AS Lineitem(l_orderkey, l_extendedprice, l_discount)
)
SELECT c.c_name, o.o_orderstatus, l.l_extendedprice
FROM CustomerCTE c
JOIN OrderCTE o ON c.c_custkey = o.o_custkey
JOIN LineitemCTE l ON o.o_orderkey = l.l_orderkey
WHERE EXISTS (
    SELECT *
    FROM (
        VALUES ('Region1'),
               ('Region2')
    ) AS Region(r_name)
    JOIN (
        VALUES (1, 'Region1'),
               (2, 'Region2')
    ) AS Nation(n_nationkey, n_regionkey) ON Region.r_name = Nation.n_regionkey
    WHERE c.c_address LIKE 'Address%'
    AND Nation.n_nationkey = 1
);
