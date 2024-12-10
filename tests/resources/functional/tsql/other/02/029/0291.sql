-- tsql sql:
DROP TABLE IF EXISTS customer_orders;
CREATE TABLE customer_orders
(
    order_key INT,
    customer_key INT,
    order_status VARCHAR(10)
);
INSERT INTO customer_orders (order_key, customer_key, order_status)
SELECT 1, 1, 'active'
FROM (VALUES (1, 1, 'active')) AS t (order_key, customer_key, order_status);
SELECT *
FROM customer_orders;
-- REMORPH CLEANUP: DROP TABLE customer_orders;
