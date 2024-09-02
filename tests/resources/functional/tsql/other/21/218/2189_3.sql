--Query type: DDL
CREATE TABLE customer_orders
    WITH (DISTRIBUTION = HASH (customer_id)) AS
SELECT *
FROM (VALUES (1, 'John', 100.0), (2, 'Jane', 200.0), (3, 'Bob', 50.0)) AS customer_temp (customer_id, customer_name, order_total);
-- REMORPH CLEANUP: DROP TABLE customer_orders;