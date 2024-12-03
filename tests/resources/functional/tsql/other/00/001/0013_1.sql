--Query type: DDL
CREATE TABLE customer_orders (order_key INT DEFAULT (NEXT VALUE FOR order_sequence), customer_name VARCHAR(50), order_total DECIMAL(10, 2));
INSERT INTO customer_orders (customer_name, order_total)
SELECT 'John Doe', 100.00;
SELECT * FROM customer_orders;
