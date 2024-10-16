--Query type: DQL
WITH temp_result AS (
    SELECT 'John Joe' AS customer_name, 1 AS customer_id
    UNION ALL
    SELECT 'Jane Doe', 2
    UNION ALL
    SELECT 'Joe Johnson', 3
    UNION ALL
    SELECT 'Emily Chen', 4
)
SELECT *
FROM temp_result
WHERE customer_name LIKE '%Jo%oe%'
    OR customer_name LIKE 'T%e'
ORDER BY customer_name;