-- tsql sql:
WITH temp_result AS ( SELECT * FROM customer WHERE c_nationkey = 1 ) SELECT * FROM temp_result WHERE c_name = 'Customer#000000001';
