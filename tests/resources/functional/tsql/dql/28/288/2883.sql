--Query type: DQL
WITH customer_info AS (
    SELECT customer_name, customer_address
    FROM (
        VALUES ('Customer1', 'Address1'),
               ('Customer2', 'Address2')
    ) AS customer (customer_name, customer_address)
),
order_info AS (
    SELECT order_id, order_date
    FROM (
        VALUES (1, '2022-01-01'),
               (2, '2022-01-02')
    ) AS orders (order_id, order_date)
)
SELECT c.customer_name, o.order_date
FROM customer_info c
JOIN order_info o ON c.customer_name = o.order_id
WHERE c.customer_name = 'Customer1';
