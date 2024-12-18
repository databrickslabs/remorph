-- tsql sql:
WITH temp AS ( SELECT 'Name' AS emp_name, NULL AS emp_middlename, 'Lastname' AS emp_lastname ) SELECT CONCAT (emp_name, emp_middlename, emp_lastname) AS Result FROM temp;
