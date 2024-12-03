--Query type: DQL
WITH temp_result AS ( SELECT o_orderkey, o_custkey, o_orderstatus, o_totalprice FROM ( VALUES (1, 1, 'O', 100.0), (2, 2, 'O', 200.0), (3, 3, 'O', 300.0) ) AS orders (o_orderkey, o_custkey, o_orderstatus, o_totalprice) ) SELECT o_orderkey, OBJECT_NAME(o_orderkey) AS order_name, o_custkey, o_orderstatus FROM temp_result WHERE o_orderstatus LIKE '[^O]%'
