--Query type: DDL
CREATE TABLE customer_temp (c_custkey INT, c_name VARCHAR(255), c_address VARCHAR(255));
INSERT INTO customer_temp (c_custkey, c_name, c_address)
VALUES (1, 'Customer#000000001', 'Smith'), (2, 'Customer#000000002', 'Johnson');
SELECT * FROM customer_temp;
-- REMORPH CLEANUP: DROP TABLE customer_temp;
