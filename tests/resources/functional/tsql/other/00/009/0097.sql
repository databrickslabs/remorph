--Query type: DDL
WITH customer_iv AS (
    SELECT 1 AS id, 'John Doe' AS name, 'john.doe@example.com' AS email
)
SELECT *
FROM customer_iv;
