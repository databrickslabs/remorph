--Query type: DQL
WITH ranked_orders AS (
    SELECT o_orderkey, o_custkey, o_totalprice, ROW_NUMBER() OVER (PARTITION BY o_custkey ORDER BY o_totalprice DESC) AS row_num
    FROM (
        VALUES (1, 1, 100.0),
               (2, 1, 200.0),
               (3, 2, 50.0)
    ) AS orders (o_orderkey, o_custkey, o_totalprice)
)
SELECT TOP 10 c.c_name, c.c_address, SUM(ro.o_totalprice) AS total_revenue, COUNT(DISTINCT ro.o_orderkey) AS num_orders
FROM (
    VALUES ('Customer1', 'Address1', 1, 1),
           ('Customer2', 'Address2', 2, 1)
) AS c (c_name, c_address, c_custkey, c_nationkey)
JOIN ranked_orders ro ON c.c_custkey = ro.o_custkey
WHERE c.c_nationkey = 1 AND ro.row_num <= 5
GROUP BY c.c_name, c.c_address
ORDER BY total_revenue DESC;