-- tsql sql:
WITH customers AS (
    SELECT *
    FROM (
        VALUES
            (1, 'John'),
            (2, 'Alice')
    ) AS c (customer_id, customer_name)
),
orders AS (
    SELECT *
    FROM (
        VALUES
            (1, 100, 1),
            (2, 200, 2)
    ) AS o (order_id, total_amount, customer_id)
)
SELECT
    c.customer_id,
    c.customer_name,
    o.order_id,
    o.total_amount,
    o.customer_id AS customer_id_order
FROM
    customers c
INNER JOIN orders o
    ON c.customer_id = o.customer_id;
