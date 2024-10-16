--Query type: TCL
BEGIN TRANSACTION;

WITH orders_cte AS (
    SELECT *
    FROM (
        VALUES (
            (1, 1, '2020-01-01'),
            (2, 2, '2020-01-02'),
            (3, 3, '2020-01-03')
        )
    ) AS orders (order_id, customer_id, order_date)
),
updated_orders_cte AS (
    SELECT 1 AS order_id, 1 AS customer_id, '2020-01-04' AS order_date
)

INSERT INTO customer_orders (customer_id, order_id, order_date)
SELECT customer_id, order_id, order_date
FROM orders_cte
UNION ALL
SELECT customer_id, order_id, order_date
FROM updated_orders_cte;

COMMIT;