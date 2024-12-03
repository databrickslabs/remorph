--Query type: DQL
SELECT CAST(orders.order_key AS BINARY(4)) AS [order_key] FROM (VALUES (1, 2, 3)) AS orders ([order_key], [order_status], [total_price]);
