--Query type: DQL
WITH CustomerCTE AS (
    SELECT c_custkey, c_nationkey, c_acctbal
    FROM (
        VALUES (1, 1, 100.0),
               (2, 2, 200.0),
               (3, 3, 300.0)
    ) AS Customer(c_custkey, c_nationkey, c_acctbal)
),
OrderCTE AS (
    SELECT o_orderkey, o_custkey, o_totalprice
    FROM (
        VALUES (1, 1, 1000.0),
               (2, 2, 2000.0),
               (3, 3, 3000.0)
    ) AS Orders(o_orderkey, o_custkey, o_totalprice)
),
NationCTE AS (
    SELECT n_nationkey, n_name
    FROM (
        VALUES (1, 'USA'),
               (2, 'Canada'),
               (3, 'Mexico')
    ) AS Nation(n_nationkey, n_name)
)
SELECT c.c_nationkey,
       NTILE(2) OVER (PARTITION BY c.c_nationkey ORDER BY SUM(o.o_totalprice) DESC) AS Quartile,
       CONVERT(VARCHAR(13), SUM(o.o_totalprice), 1) AS TotalPrice,
       n.n_name AS NationName
FROM CustomerCTE c
INNER JOIN OrderCTE o ON c.c_custkey = o.o_custkey
INNER JOIN NationCTE n ON c.c_nationkey = n.n_nationkey
WHERE o.o_orderkey = 1
GROUP BY c.c_nationkey, n.n_name
ORDER BY n.n_name, Quartile;