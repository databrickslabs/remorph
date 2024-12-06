-- tsql sql:
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
WITH customer_sales AS (
    SELECT 1 AS c_custkey, 100.0 AS total_sales
)
SELECT * FROM customer_sales;
