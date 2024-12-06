-- tsql sql:
WITH temp_result AS ( SELECT c_custkey, c_nationkey FROM (VALUES (1, 1), (2, 2), (3, 3)) AS temp(c_custkey, c_nationkey) ) SELECT c_custkey FROM temp_result WHERE c_nationkey = DB_ID();
