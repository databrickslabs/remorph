--Query type: DML
WITH temp_result AS ( SELECT * FROM my_function() ) SELECT * FROM temp_result;
