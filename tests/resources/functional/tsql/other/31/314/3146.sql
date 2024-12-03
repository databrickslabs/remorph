--Query type: DDL
WITH orders AS (
    SELECT *
    FROM (
        VALUES
            (1, 100, '2020-01-01', 1),
            (2, 200, '2020-01-02', 1),
            (3, 300, '2020-01-03', 2)
    ) AS orders (order_id, order_total, order_date, customer_id)
)
SELECT *
FROM orders;
