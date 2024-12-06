-- tsql sql:
SELECT l_orderkey, CASE WHEN l_orderkey = 1 THEN 'one' WHEN l_orderkey = 2 THEN 'two' WHEN l_orderkey IS NULL THEN 'NULL' ELSE 'other' END AS result FROM (VALUES (1), (2), (NULL)) AS lineitem (l_orderkey);
