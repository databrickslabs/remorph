--Query type: DQL
SELECT AVG(l_extendedprice) FROM (VALUES (1, 10.0), (2, 20.0), (3, 30.0)) AS Lineitem (l_orderkey, l_extendedprice);
