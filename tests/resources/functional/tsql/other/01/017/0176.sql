--Query type: DDL
WITH customer_data AS (
    SELECT c_custkey, c_nationkey, c_acctbal
    FROM (
        VALUES (1, 1, 100.00),
               (2, 2, 200.00)
    ) AS customer (c_custkey, c_nationkey, c_acctbal)
),
orders_data AS (
    SELECT o_orderkey, o_custkey, o_totalprice
    FROM (
        VALUES (1, 1, 1000.00),
               (2, 2, 2000.00)
    ) AS orders (o_orderkey, o_custkey, o_totalprice)
)
SELECT 'customer_data' AS source, c_custkey, c_nationkey, c_acctbal
FROM customer_data
UNION ALL
SELECT 'orders_data' AS source, o_orderkey, o_custkey, o_totalprice
FROM orders_data;