--Query type: DQL
SELECT ROUND(T1.order_total, 0) AS rounded_order_total FROM (VALUES (150.75)) AS T1(order_total);
