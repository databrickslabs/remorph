--Query type: DQL
SELECT CASE WHEN T2.order_total IS NOT NULL THEN T2.order_total ELSE 100.0 END AS total_amount FROM (VALUES (1, 10.0), (2, NULL), (3, 30.0)) AS T1(customer_id, order_total) CROSS JOIN (SELECT order_id, order_total FROM (VALUES (1, 10.0), (2, 20.0), (3, NULL)) AS T3(order_id, order_total)) AS T2
