-- tsql sql:
WITH temp_result AS ( SELECT c_custkey, c_nationkey FROM customer ) SELECT GROUPING_ID(c_custkey, c_nationkey) FROM temp_result GROUP BY CUBE(c_custkey, c_nationkey)
