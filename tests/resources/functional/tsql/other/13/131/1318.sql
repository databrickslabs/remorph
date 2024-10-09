--Query type: DDL
CREATE TABLE customer_orders
(
    order_key INT NOT NULL,
    customer_name VARCHAR(20),
    order_status VARCHAR(6)
)
WITH (DISTRIBUTION = REPLICATE);

CREATE CLUSTERED INDEX idx_customer_name
ON customer_orders (customer_name);

-- REMORPH CLEANUP: DROP TABLE customer_orders;
-- REMORPH CLEANUP: DROP INDEX idx_customer_name ON customer_orders;

SELECT *
FROM customer_orders;