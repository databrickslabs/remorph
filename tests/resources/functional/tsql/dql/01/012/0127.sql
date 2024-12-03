--Query type: DQL
WITH orders_cte AS ( SELECT 1 AS order_id ) SELECT CURRENT_TIMESTAMP FROM orders_cte;
