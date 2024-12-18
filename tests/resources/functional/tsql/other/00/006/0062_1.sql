-- tsql sql:
WITH customers AS (
    SELECT *
    FROM (
        VALUES
            (1, 'John Doe', '123 Main St'),
            (2, 'Jane Doe', '456 Elm St')
    ) AS c (customer_id, customer_name, address)
),
orders AS (
    SELECT *
    FROM (
        VALUES
            (1, 1, '2020-01-01'),
            (2, 1, '2020-01-15'),
            (3, 2, '2020-02-01')
    ) AS o (order_id, customer_id, order_date)
)
SELECT
    c.customer_id,
    c.customer_name,
    c.address,
    o.order_id,
    o.order_date
FROM
    customers c
    INNER JOIN orders o ON c.customer_id = o.customer_id;
