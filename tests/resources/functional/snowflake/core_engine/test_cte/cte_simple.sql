-- snowflake sql:
WITH employee_hierarchy AS (
    SELECT
        employee_id,
        manager_id,
        employee_name
    FROM
        employees
    WHERE
        manager_id IS NULL
)
SELECT *
FROM employee_hierarchy;

-- databricks sql:
WITH employee_hierarchy AS (SELECT employee_id, manager_id, employee_name FROM employees WHERE manager_id IS NULL) SELECT * FROM employee_hierarchy;
