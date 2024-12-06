-- tsql sql:
SELECT l_orderkey, l_extendedprice, LAST_VALUE(l_extendedprice) OVER (PARTITION BY l_orderkey ORDER BY l_extendedprice) AS l_extendedprice_last FROM (VALUES (1, 10.0), (1, 11.0), (1, 12.0), (2, 20.0), (2, 21.0), (2, 22.0)) AS lineitem (l_orderkey, l_extendedprice);
