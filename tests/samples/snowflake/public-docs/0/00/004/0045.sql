SELECT department_name, last_name, first_name
    FROM employee_table INNER JOIN department_table
        ON employee_table.department_ID = department_table.department_ID
    ORDER BY department_name, last_name, first_name;