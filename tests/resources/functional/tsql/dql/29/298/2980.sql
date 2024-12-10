-- tsql sql:
WITH temp_result AS ( SELECT value FROM GENERATE_SERIES(1, 10, 1) ) SELECT value FROM temp_result
