--Query type: DDL
SELECT 1 AS order_key, 1 AS customer_key, 'active' AS order_status INTO customer_orders FROM (VALUES (1, 1, 'active')) AS t(order_key, customer_key, order_status); SELECT * FROM customer_orders; -- REMORPH CLEANUP: DROP TABLE customer_orders;
