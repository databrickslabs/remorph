-- tsql sql:
WITH customer_hierarchy AS (
    SELECT customer_key, nation_key, account_balance
    FROM (
        VALUES
            (1, 1, 100.0),
            (2, 2, 200.0),
            (3, 3, 300.0)
    ) AS customer_hierarchy (customer_key, nation_key, account_balance)
)
SELECT *
FROM customer_hierarchy
ORDER BY customer_key;
