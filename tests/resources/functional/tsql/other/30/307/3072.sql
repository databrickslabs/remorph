-- tsql sql:
WITH customer AS (
    SELECT 1 AS custkey, 'Customer1' AS name, 1 AS nationkey
), orders AS (
    SELECT 1 AS orderkey, 1 AS custkey, 1000.0 AS totalprice
)
SELECT *
FROM customer;

SELECT *
FROM orders;
