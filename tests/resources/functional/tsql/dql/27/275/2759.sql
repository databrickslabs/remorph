-- tsql sql:
SELECT STDEV(o_totalprice) FROM (VALUES (1, 100.0), (2, 200.0), (3, 300.0)) AS orders(o_orderkey, o_totalprice);
