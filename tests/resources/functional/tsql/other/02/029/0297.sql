-- tsql sql:
CREATE TABLE customer_data
(
    customer_key BINARY(32),
    customer_name BINARY(50),
    customer_address BINARY,
    customer_email BINARY
);

WITH customer_data_cte AS
(
    SELECT HASHBYTES('SHA2_256', 'Customer1') AS customer_key,
           CONVERT(VARBINARY(50), 'John Doe', 2) AS customer_name,
           CONVERT(VARBINARY(MAX), '123 Main St', 2) AS customer_address,
           CONVERT(VARBINARY(MAX), 'john.doe@example.com', 2) AS customer_email
)
INSERT INTO customer_data (customer_key, customer_name, customer_address, customer_email)
SELECT customer_key, customer_name, customer_address, customer_email
FROM customer_data_cte;

SELECT * FROM customer_data;
-- REMORPH CLEANUP: DROP TABLE customer_data;
