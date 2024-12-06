-- tsql sql:
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
SELECT DISTINCT c.c_name, o.o_orderstatus, l.l_extendedprice
FROM CustomerCTE c
INNER JOIN OrderCTE o ON c.c_custkey = o.o_custkey
INNER JOIN LineitemCTE l ON o.o_orderkey = l.l_orderkey
WHERE l.l_discount IN (
    SELECT l_discount
    FROM (
        VALUES (0.1),
               (0.2)
    ) AS Discount(l_discount)
    WHERE l_discount IN (
        SELECT l_discount
        FROM (
            VALUES (0.1),
                   (0.3)
        ) AS Discount2(l_discount)
        WHERE l_discount LIKE '%.1'
    )
)
ORDER BY c.c_name;
