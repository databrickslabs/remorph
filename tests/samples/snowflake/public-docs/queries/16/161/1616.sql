-- see https://docs.snowflake.com/en/sql-reference/operators-subquery

SELECT department_id
FROM departments d
WHERE NOT EXISTS (SELECT 1
                  FROM employees e
                  WHERE e.department_id = d.department_id);