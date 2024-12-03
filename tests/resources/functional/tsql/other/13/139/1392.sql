--Query type: DCL
WITH orders AS (
    SELECT *
    FROM (
        VALUES
            (1, 100, '2020-01-01'),
            (2, 200, '2020-01-02'),
            (3, 300, '2020-01-03')
    ) AS orders (order_id, order_total, order_date)
),
 customers AS (
    SELECT *
    FROM (
        VALUES
            (1, 'Customer1'),
            (2, 'Customer2'),
            (3, 'Customer3')
    ) AS customers (customer_id, customer_name)
),
 filtered_orders AS (
    SELECT order_id
    FROM orders
    WHERE order_total > 100
)
SELECT
    o.order_id,
    c.customer_name,
    SUM(o.order_total) AS total_revenue
FROM
    orders o
    INNER JOIN customers c ON o.order_id = c.customer_id
    INNER JOIN filtered_orders fo ON o.order_id = fo.order_id
WHERE
    o.order_date >= '2020-01-01'
GROUP BY
    o.order_id,
    c.customer_name
HAVING
    SUM(o.order_total) > 1000
ORDER BY
    total_revenue DESC;
