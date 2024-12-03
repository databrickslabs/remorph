--Query type: DQL
SELECT * FROM (VALUES (1, 'customer1', 100.0), (2, 'customer2', 200.0), (3, 'customer3', 300.0)) AS customer_table (customer_id, customer_name, order_total);
