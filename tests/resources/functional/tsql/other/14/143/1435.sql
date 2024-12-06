-- tsql sql:
WITH temp_result AS (
    SELECT 'INDIA' AS n_name, 'ASIA' AS r_name, 1000.0 AS revenue
    UNION ALL
    SELECT 'CHINA', 'ASIA', 2000.0
    UNION ALL
    SELECT 'USA', 'AMERICA', 3000.0
)
SELECT n_name, r_name, revenue
FROM temp_result
WHERE r_name = 'ASIA'
ORDER BY revenue DESC
