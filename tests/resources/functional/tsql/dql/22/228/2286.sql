--Query type: DQL
WITH customer_data AS (
    SELECT customer_name, customer_address
    FROM (
        VALUES ('Customer1', 'Address1'),
               ('Customer2', 'Address2')
    ) AS customers (customer_name, customer_address)
)
SELECT customer_name, customer_address
FROM customer_data
WHERE customer_name LIKE 'Customer%'
ORDER BY customer_name ASC;
