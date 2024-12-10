-- tsql sql:
WITH temp_result_set AS (
    SELECT 'Sales' AS department, 'Smith' AS lastname, 10.0 AS rate, '2020-01-01' AS hiredate
    UNION ALL
    SELECT 'Marketing', 'Johnson', 15.0, '2020-02-01'
    UNION ALL
    SELECT 'Sales', 'Williams', 12.0, '2020-03-01'
),
    temp_result_set2 AS (
    SELECT 'Sales' AS department, 'Smith' AS lastname, 10.0 AS rate, '2020-01-01' AS hiredate
    UNION ALL
    SELECT 'Marketing', 'Johnson', 15.0, '2020-02-01'
    UNION ALL
    SELECT 'Sales', 'Williams', 12.0, '2020-03-01'
)
SELECT trs1.department, trs1.lastname, trs1.rate, trs1.hiredate, LAST_VALUE(trs1.hiredate) OVER (PARTITION BY trs1.department ORDER BY trs1.rate) AS LastValue
FROM temp_result_set trs1
INNER JOIN temp_result_set2 trs2 ON trs2.department = trs1.department
WHERE trs1.department IN ('Sales', 'Marketing');
