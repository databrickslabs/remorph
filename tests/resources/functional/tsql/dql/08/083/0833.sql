--Query type: DQL
WITH d AS (
    SELECT *
    FROM (
        VALUES (1, 'Sales'),
               (2, 'Marketing')
    ) AS d(department_ID, department_name)
),
     e AS (
    SELECT *
    FROM (
        VALUES (1, 1, 'John'),
               (2, 1, 'Jane')
    ) AS e(employee_ID, department_ID, employee_name)
)
SELECT *
FROM d
CROSS APPLY (
    SELECT *
    FROM e
    WHERE e.department_ID = d.department_ID
) AS iv2
ORDER BY iv2.employee_ID;
