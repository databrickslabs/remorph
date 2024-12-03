--Query type: DDL
CREATE TABLE customer_authz (c_custkey INT, c_name VARCHAR(50), c_address VARCHAR(100));
WITH customer_data AS (
    SELECT c_custkey, c_name, c_address
    FROM (
        VALUES (1, 'Customer 1', 'Address 1'),
               (2, 'Customer 2', 'Address 2'),
               (3, 'Customer 3', 'Address 3')
    ) AS customer (c_custkey, c_name, c_address)
)
INSERT INTO customer_authz (c_custkey, c_name, c_address)
SELECT c_custkey, c_name, c_address
FROM customer_data;
SELECT * FROM customer_authz;
-- REMORPH CLEANUP: DROP TABLE customer_authz;
