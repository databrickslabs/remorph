-- tsql sql:
WITH customer_info AS (
    SELECT customer_key, customer_name
    FROM (
        VALUES (1, 'Customer1'),
               (2, 'Customer2')
    ) AS customer(customer_key, customer_name)
),
order_info AS (
    SELECT order_key, order_date
    FROM (
        VALUES (1, '2020-01-01'),
               (2, '2020-01-02')
    ) AS orders(order_key, order_date)
)
SELECT c.customer_key, c.customer_name, o.order_key, o.order_date
FROM customer_info c
INNER JOIN order_info o ON c.customer_key = o.order_key
WHERE c.customer_name = 'Customer1' AND o.order_date = '2020-01-01';
