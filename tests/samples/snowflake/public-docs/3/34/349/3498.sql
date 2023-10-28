SELECT emp.employee_ID, emp.last_name, index, value AS project_name
    FROM employees AS emp, LATERAL FLATTEN(INPUT => emp.project_names) AS proj_names
    ORDER BY employee_ID;