--Query type: DQL
WITH EmployeeHistory AS (
    SELECT 'Sales' AS Department, 'Smith' AS LastName, 10000.0 AS Rate
    UNION ALL
    SELECT 'Marketing', 'Johnson', 8000.0
    UNION ALL
    SELECT 'Sales', 'Williams', 12000.0
)
SELECT
    Department,
    LastName,
    Rate,
    CUME_DIST() OVER (PARTITION BY Department ORDER BY Rate) AS CumeDist,
    PERCENT_RANK() OVER (PARTITION BY Department ORDER BY Rate) AS PctRank
FROM
    EmployeeHistory
WHERE
    Department IN ('Sales', 'Marketing')
ORDER BY
    Department,
    Rate DESC;
