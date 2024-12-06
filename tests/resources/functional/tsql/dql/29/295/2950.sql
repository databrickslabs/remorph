-- tsql sql:
WITH orders AS ( SELECT order_id, customer_id FROM ( VALUES (1, 10), (2, 20), (3, 30) ) AS orders (order_id, customer_id) ) SELECT order_id FROM orders WHERE customer_id = 10;
