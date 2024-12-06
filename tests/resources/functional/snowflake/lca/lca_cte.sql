-- snowflake sql:
WITH cte AS (SELECT column_a as customer_id
    FROM my_table
    WHERE customer_id = '123')
SELECT * FROM cte;

-- databricks sql:
WITH cte AS (SELECT column_a as customer_id
    FROM my_table
    WHERE column_a = '123')
SELECT * FROM cte;
