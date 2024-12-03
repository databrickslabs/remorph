--Query type: DQL
SELECT l_orderkey, AVG(l_discount) OVER (PARTITION BY l_orderkey) AS avg_discount FROM (VALUES (1, 0.1), (2, 0.2), (3, 0.3), (1, 0.1), (2, 0.2), (3, 0.3)) AS lineitem (l_orderkey, l_discount) ORDER BY l_orderkey;
