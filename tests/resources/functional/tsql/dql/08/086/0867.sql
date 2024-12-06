-- tsql sql:
WITH temp_result AS ( SELECT * FROM ( VALUES ('customer1', 100), ('customer2', 200) ) AS customers (name, id) ) SELECT * FROM temp_result;
