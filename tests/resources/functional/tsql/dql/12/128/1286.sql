--Query type: DQL
SELECT customer_name, order_date FROM (VALUES ('Customer1', '2020-01-01'), ('Customer2', '2020-01-02')) AS customer_orders (customer_name, order_date);
