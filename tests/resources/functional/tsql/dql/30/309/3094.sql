--Query type: DQL
WITH CustomerCTE AS (
    SELECT c_custkey, c_nationkey, c_acctbal
    FROM (
        VALUES (1, 1, 100.00),
               (2, 2, 200.00),
               (3, 3, 300.00)
    ) AS Customer(c_custkey, c_nationkey, c_acctbal)
),
OrderCTE AS (
    SELECT o_orderkey, o_custkey, o_totalprice
    FROM (
        VALUES (1, 1, 1000.00),
               (2, 2, 2000.00),
               (3, 3, 3000.00)
    ) AS Orders(o_orderkey, o_custkey, o_totalprice)
)
SELECT c.c_nationkey, MAX(o.o_totalprice) AS MaximumTotalPrice
FROM CustomerCTE c
INNER JOIN OrderCTE o ON c.c_custkey = o.o_custkey
GROUP BY c.c_nationkey
HAVING (
    MAX(CASE WHEN c.c_acctbal > 0 THEN o.o_totalprice ELSE NULL END) > 1000.00
    OR MAX(CASE WHEN c.c_acctbal <= 0 THEN o.o_totalprice ELSE NULL END) > 500.00
)
ORDER BY MaximumTotalPrice DESC;