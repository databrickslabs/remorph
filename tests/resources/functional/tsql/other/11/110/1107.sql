--Query type: DDL
CREATE TABLE #ExpenseQueue
(
    order_total decimal(10, 2),
    order_date date,
    customer_id int,
    product_name varchar(50)
);

INSERT INTO #ExpenseQueue
(
    order_total,
    order_date,
    customer_id,
    product_name
)
VALUES
(
    1000.0,
    '2020-01-01',
    1,
    'Product A'
),
(
    500.0,
    '2020-01-02',
    2,
    'Product B'
),
(
    2000.0,
    '2020-01-03',
    1,
    'Product C'
);

WITH orders AS
(
    SELECT order_total, order_date, customer_id, product_name
    FROM #ExpenseQueue
)
SELECT TOP 10
    CASE
        WHEN SUM(CASE WHEN order_total > 1000 THEN 1 ELSE 0 END) > 0 THEN 'High'
        ELSE 'Low'
    END AS order_category,
    SUM(order_total) AS total_revenue,
    AVG(order_total) AS average_order,
    MAX(order_total) AS max_order,
    MIN(order_total) AS min_order,
    COUNT(DISTINCT customer_id) AS unique_customers,
    STRING_AGG(product_name, ', ') AS products
FROM orders
WHERE order_date >= '2020-01-01'
GROUP BY customer_id
HAVING SUM(order_total) > 1000
ORDER BY total_revenue DESC;
-- REMORPH CLEANUP: DROP TABLE #ExpenseQueue;
