--Query type: DQL
WITH cte1 AS (
    SELECT o_orderkey, o_totalprice, o_orderdate
    FROM (
        VALUES (1, 100.0, '2020-01-01'),
               (2, 200.0, '2020-01-02'),
               (3, 300.0, '2020-01-03')
    ) AS o(o_orderkey, o_totalprice, o_orderdate)
),
cte2 AS (
    SELECT o_orderkey, MAX(o_orderdate) AS max_orderdate
    FROM cte1
    GROUP BY o_orderkey
)
SELECT TOP(10) cte1.o_orderkey, cte1.o_totalprice, RANK() OVER (ORDER BY cte1.o_totalprice DESC) AS RankByTotalPrice
FROM cte1
INNER JOIN cte2 ON cte1.o_orderkey = cte2.o_orderkey
WHERE cte1.o_orderdate = cte2.max_orderdate
ORDER BY cte1.o_orderkey;