--Query type: DQL
SELECT l_orderkey, l_discount, GREATEST(l_orderkey, l_discount) AS greatest FROM (VALUES (1, 0.1), (2, 0.2), (3, 0.3)) AS lineitem (l_orderkey, l_discount) ORDER BY l_orderkey;
