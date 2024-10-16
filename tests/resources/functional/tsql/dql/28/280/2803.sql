--Query type: DQL
WITH CustomerCTE AS (
    SELECT customer_key, customer_name
    FROM (
        VALUES (1, 'Customer1'),
               (2, 'Customer2')
    ) AS Customer(customer_key, customer_name)
),
OrderCTE AS (
    SELECT order_key, customer_key, order_date
    FROM (
        VALUES (1, 1, '2020-01-01'),
               (2, 1, '2020-01-15'),
               (3, 2, '2020-02-01')
    ) AS Orders(order_key, customer_key, order_date)
)
SELECT C.*
FROM CustomerCTE AS C
JOIN OrderCTE AS O
    ON C.customer_key = O.customer_key
WHERE O.order_date > '2020-01-01'
    AND C.customer_name = 'Customer1';