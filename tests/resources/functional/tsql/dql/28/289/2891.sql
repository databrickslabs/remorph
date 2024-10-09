--Query type: DQL
WITH CustomerCTE AS (
    SELECT c_custkey, c_acctbal
    FROM (
        VALUES (1, 100.00),
               (2, 200.00),
               (3, 300.00)
    ) AS Customer(c_custkey, c_acctbal)
),
OrderCTE AS (
    SELECT o_orderkey, o_totalprice
    FROM (
        VALUES (1, 1000.00),
               (2, 2000.00),
               (3, 3000.00)
    ) AS Orders(o_orderkey, o_totalprice)
)
SELECT c.c_custkey, c.c_acctbal, o.o_totalprice
FROM CustomerCTE AS c
INNER JOIN OrderCTE AS o WITH (FORCESCAN) ON c.c_custkey = o.o_orderkey
WHERE c.c_acctbal > 100 AND (o.o_totalprice > 500 OR o.o_totalprice < 2500.00)