--Query type: DDL
CREATE TABLE customer_orders (order_key int NOT NULL, cust_name varchar(20), order_total decimal(10, 2));
INSERT INTO customer_orders (order_key, cust_name, order_total)
VALUES (1, 'John Doe', 100.00), (2, 'Jane Doe', 200.00);
SELECT * FROM customer_orders;
-- REMORPH CLEANUP: DROP TABLE customer_orders;