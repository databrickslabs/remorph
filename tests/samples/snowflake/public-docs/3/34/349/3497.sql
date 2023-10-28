UPDATE employees SET project_names = ARRAY_CONSTRUCT('Materialized Views', 'UDFs') 
    WHERE employee_ID = 101;
UPDATE employees SET project_names = ARRAY_CONSTRUCT('Materialized Views', 'Lateral Joins')
    WHERE employee_ID = 102;