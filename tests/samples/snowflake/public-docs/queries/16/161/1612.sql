-- see https://docs.snowflake.com/en/sql-reference/constructs/where

SELECT d.department_name, p.project_name, e.employee_name
    FROM  departments d, projects p, employees e
    WHERE
            p.department_id = d.department_id
        AND
            e.project_id = p.project_id
    ORDER BY d.department_id, p.project_id, e.employee_id;