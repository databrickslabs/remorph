-- tsql sql:
WITH departments AS (
    SELECT *
    FROM (
        VALUES (1, 'Sales'),
               (2, 'Marketing')
    ) AS d (department_ID, department_name)
),
employees AS (
    SELECT *
    FROM (
        VALUES (1, 1, 'John'),
               (2, 1, 'Alice'),
               (3, 2, 'Bob')
    ) AS e (employee_ID, department_ID, employee_name)
)
SELECT *
FROM departments d
CROSS APPLY (
    SELECT *
    FROM employees e
    WHERE e.department_ID = d.department_ID
) AS iv2
ORDER BY employee_ID;
