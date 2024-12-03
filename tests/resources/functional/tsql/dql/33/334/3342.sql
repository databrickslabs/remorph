--Query type: DQL
WITH EmployeeHistory AS (
    SELECT 'Sales' AS Department, 'Smith' AS LastName, 10000.0 AS Rate
    UNION ALL
    SELECT 'Marketing', 'Johnson', 20000.0
    UNION ALL
    SELECT 'Sales', 'Williams', 30000.0
),
PayHistory AS (
    SELECT 'Sales' AS Department, 'Smith' AS LastName, 10000.0 AS Rate
    UNION ALL
    SELECT 'Marketing', 'Johnson', 20000.0
    UNION ALL
    SELECT 'Sales', 'Williams', 30000.0
)
SELECT
    eh.Department,
    eh.LastName,
    eh.Rate,
    CUME_DIST() OVER (PARTITION BY eh.Department ORDER BY eh.Rate) AS CumeDist,
    PERCENT_RANK() OVER (PARTITION BY eh.Department ORDER BY eh.Rate) AS PctRank
FROM
    EmployeeHistory AS eh
    INNER JOIN PayHistory AS ph ON ph.Department = eh.Department
WHERE
    eh.Department IN ('Sales', 'Marketing')
ORDER BY
    eh.Department,
    eh.Rate DESC;
