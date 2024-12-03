--Query type: DDL
WITH orders AS ( SELECT 1 AS o_orderkey, 2 AS o_custkey, 'A' AS o_orderstatus, 10.0 AS o_totalprice UNION ALL SELECT 3, 4, 'B', 20.0 ) SELECT * FROM orders;
