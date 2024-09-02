--Query type: DQL
SELECT order_total, order_date FROM (VALUES (100.00, '2022-01-01'), (200.00, '2022-01-15'), (300.00, '2022-02-01')) AS orders (order_total, order_date) WHERE order_total > 150.00;