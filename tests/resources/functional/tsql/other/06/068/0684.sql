-- tsql sql:
CREATE TABLE orders
(
    customer_id INT,
    order_year INT,
    total_amount DECIMAL(10, 2)
);

WITH orders_cte AS
(
    SELECT 1 AS customer_id, 2015 AS order_year, 2000.00 AS total_amount
    UNION ALL
    SELECT 2, 2016, 3000.00
    UNION ALL
    SELECT 3, 2017, 4000.00
    UNION ALL
    SELECT 4, 2018, 5000.00
)
INSERT INTO orders (customer_id, order_year, total_amount)
SELECT customer_id, order_year, total_amount
FROM orders_cte;

SELECT *
FROM orders;
-- REMORPH CLEANUP: DROP TABLE orders;
