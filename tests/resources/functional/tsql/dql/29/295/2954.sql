-- tsql sql:
WITH temp_result AS ( SELECT l_extendedprice AS result, l_discount AS d FROM lineitem ) SELECT result, result * d AS calculated_result FROM temp_result;
