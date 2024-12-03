--Query type: DDL
WITH orders AS ( SELECT o_orderkey, o_totalprice FROM ( VALUES (1, 10), (2, 20), (3, 30), (4, 40), (5, 50) ) AS orders (o_orderkey, o_totalprice) ) SELECT o_orderkey, COUNT(*) AS total_orders FROM orders WHERE o_orderkey < 3 GROUP BY o_orderkey;
