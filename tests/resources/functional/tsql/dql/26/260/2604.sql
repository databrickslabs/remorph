-- tsql sql:
WITH temp_result AS ( SELECT 123.45 AS num1, -123.45 AS num2, 123.45 AS num3 ) SELECT FLOOR(num1) AS floor_num1, FLOOR(num2) AS floor_num2, FLOOR(num3) AS floor_num3 FROM temp_result;