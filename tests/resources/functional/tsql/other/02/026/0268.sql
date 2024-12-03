--Query type: DDL
CREATE TABLE customer_info (c_name VARCHAR(255), c_address VARCHAR(255), c_phone VARCHAR(255));
WITH customer_data AS (
    SELECT c_name, c_address, c_phone
    FROM (
        VALUES ('John Doe', '123 Main St', '123-456-7890'),
               ('Jane Doe', '456 Elm St', '987-654-3210')
    ) AS customers (c_name, c_address, c_phone)
)
INSERT INTO customer_info
SELECT c_name, c_address, c_phone
FROM customer_data;
SELECT * FROM customer_info;
-- REMORPH CLEANUP: DROP TABLE customer_info;
