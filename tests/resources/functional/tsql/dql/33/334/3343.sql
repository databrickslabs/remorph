--Query type: DQL
WITH temp_result AS (
    SELECT comment
    FROM orders
)
SELECT comment
FROM temp_result
WHERE CONTAINS(comment, 'FORMSOF (INFLECTIONAL, ride)')
