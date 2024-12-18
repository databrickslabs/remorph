-- tsql sql:
WITH temp_result AS ( SELECT 'customer_1' AS customer_name UNION SELECT 'customer_2' AS customer_name ) SELECT customer_name FROM temp_result WHERE customer_name LIKE 'customer_%';
