-- tsql sql:
WITH customer_view AS (
    SELECT c.*, o.*
    FROM (
        VALUES (1, 'Customer1'),
               (2, 'Customer2')
    ) AS c(customer_id, customer_name)
    JOIN (
        VALUES (1, 100, 'Order1'),
               (2, 200, 'Order2')
    ) AS o(order_id, total_amount, order_name)
        ON c.customer_id = o.order_id
)
SELECT *
FROM customer_view;
