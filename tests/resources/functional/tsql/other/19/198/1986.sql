--Query type: DDL
DROP EXTERNAL TABLE #temp;

WITH temp AS (
    SELECT 'John Doe' AS employee_name, 60000 AS salary
    UNION ALL
    SELECT 'Jane Doe', 55000
    UNION ALL
    SELECT 'Bob Smith', 40000
)

SELECT
    CASE
        WHEN SUM(CASE WHEN salary > 50000 THEN 1 ELSE 0 END) > 1 THEN 'More than one high earner'
        ELSE 'One or zero high earners'
    END AS high_earner_status,
    COUNT(*) AS total_count,
    SUM(CASE WHEN salary > 50000 THEN 1 ELSE 0 END) AS high_earner_count,
    SUM(IIF(salary > 50000, 1, 0)) AS high_earner_count_iif,
    STRING_AGG(employee_name, ', ') AS employee_names
FROM temp