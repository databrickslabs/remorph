-- tsql sql:
SELECT o_orderkey, o_custkey, o_orderstatus, o_totalprice FROM (VALUES (1, 1, 'O', 100.0), (2, 2, 'O', 200.0), (3, 3, 'O', 300.0)) AS orders (o_orderkey, o_custkey, o_orderstatus, o_totalprice);
