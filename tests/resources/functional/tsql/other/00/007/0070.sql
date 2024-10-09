--Query type: DDL
WITH customers AS (
    SELECT *
    FROM (
        VALUES
            (1, 'John Doe', 'john@example.com'),
            (2, 'Jane Doe', 'jane@example.com')
    ) AS customers (customer_id, name, email)
)
SELECT
    customer_id,
    name,
    CONVERT(VARCHAR(50), email) AS email
FROM
    customers;