--Query type: DDL
CREATE TABLE customer_orders (customer_name nvarchar(255) COLLATE Latin1_General_100_CI_AS, order_date nvarchar(255) COLLATE Latin1_General_100_CI_AS);
INSERT INTO customer_orders (customer_name, order_date)
SELECT customer_name, order_date
FROM (VALUES ('John Doe', '2022-01-01'), ('Jane Doe', '2022-01-02')) AS temp_result (customer_name, order_date);
SELECT * FROM customer_orders;
-- REMORPH CLEANUP: DROP TABLE customer_orders;