SELECT * 
    FROM employees INNER JOIN dependents
        ON dependents.employee_ID = employees.id
    ORDER BY employees.id, dependents.id
    ;