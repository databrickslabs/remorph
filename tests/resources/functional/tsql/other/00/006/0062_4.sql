-- tsql sql:
CREATE TABLE customer_orders
(
    order_id INT NOT NULL,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL
);
-- REMORPH CLEANUP: DROP TABLE customer_orders;
