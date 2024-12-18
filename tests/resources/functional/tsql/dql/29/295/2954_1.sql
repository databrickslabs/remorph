-- tsql sql:
WITH temp_result AS ( SELECT 10 AS result, 2 AS d ) SELECT result, result * d AS calculation FROM temp_result;
