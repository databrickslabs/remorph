-- see https://docs.snowflake.com/en/sql-reference/functions/result_scan

SELECT * 
    FROM employees INNER JOIN dependents
        ON dependents.employee_ID = employees.id
    ORDER BY employees.id, dependents.id
    ;