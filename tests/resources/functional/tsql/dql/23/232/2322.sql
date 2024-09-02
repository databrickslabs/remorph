--Query type: DQL
WITH CustomerCTE AS (
    SELECT customer_id, customer_name
    FROM (
        VALUES (1, 'Customer1'),
               (2, 'Customer2')
    ) AS Customer(customer_id, customer_name)
),
OrderHistoryCTE AS (
    SELECT order_id, customer_id, order_date
    FROM (
        VALUES (1, 1, '2020-01-01'),
               (2, 1, '2020-01-15')
    ) AS OrderHistory(order_id, customer_id, order_date)
)
SELECT *
FROM CustomerCTE AS c WITH (SNAPSHOT)
LEFT JOIN OrderHistoryCTE AS oh
    ON c.customer_id = oh.customer_id