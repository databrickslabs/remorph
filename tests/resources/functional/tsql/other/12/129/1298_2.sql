--Query type: DDL
WITH customer_table AS (
    SELECT customer_key, customer_name, customer_address, customer_phone, customer_email
    FROM (
        VALUES (
            1, 'John Doe', '123 Main St', '123-456-7890', 'john.doe@example.com'
        )
    ) AS customer_data (
        customer_key, customer_name, customer_address, customer_phone, customer_email
    )
)
SELECT customer_key, customer_name, customer_address
FROM customer_table;