--Query type: DDL
WITH orders AS ( SELECT 1 AS orderkey, 'order1' AS orderstatus UNION ALL SELECT 2, 'order2' UNION ALL SELECT 3, 'order3' ) SELECT * FROM orders;
