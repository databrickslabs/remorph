-- tsql sql:
WITH temp_result AS ( SELECT p_name, p_type FROM part ) SELECT ROW_NUMBER() OVER ( ORDER BY p_name ASC ) AS Row#, p_name, p_type FROM temp_result WHERE p_partkey < 5;
