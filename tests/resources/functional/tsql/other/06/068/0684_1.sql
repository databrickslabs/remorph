--Query type: DML
CREATE TABLE orders (order_id INT, customer_id INT, order_date DATE, total DECIMAL(10, 2));
INSERT INTO orders (order_id, customer_id, order_date, total)
SELECT * FROM (VALUES (1, 1, '2020-01-01', 100.00), (2, 1, '2020-01-15', 200.00), (3, 2, '2020-02-01', 50.00), (4, 3, '2020-03-01', 75.00)) AS temp_result (order_id, customer_id, order_date, total);
SELECT * FROM orders;
-- REMORPH CLEANUP: DROP TABLE orders;