--Query type: DDL
CREATE TABLE customer_info (customer_id INT, customer_name VARCHAR(255), customer_address VARCHAR(255));
INSERT INTO customer_info (customer_id, customer_name, customer_address)
VALUES (1, 'John Doe', '123 Main St'), (2, 'Jane Doe', '456 Elm St');
SELECT * FROM customer_info;
-- REMORPH CLEANUP: DROP TABLE customer_info;
