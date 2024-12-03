--Query type: DDL
CREATE TABLE orders_new
(
    order_id INT IDENTITY(500, 1),
    customer_id INT,
    order_date DATE
);

WITH orders_cte AS
(
    SELECT 1 AS customer_id, '2020-01-01' AS order_date
    UNION ALL
    SELECT 2, '2020-01-15'
    UNION ALL
    SELECT 3, '2020-02-01'
)
INSERT INTO orders_new (customer_id, order_date)
SELECT customer_id, order_date
FROM orders_cte;
-- REMORPH CLEANUP: DROP TABLE orders_new;
