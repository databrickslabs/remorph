-- tsql sql:
WITH temp_result AS ( SELECT c_custkey, o_orderkey FROM (VALUES (1, 10), (2, 20), (3, 30)) AS customer(c_custkey, o_custkey) RIGHT JOIN orders ON customer.c_custkey = orders.o_custkey ) SELECT temp_result.c_custkey FROM temp_result WHERE temp_result.o_orderkey <> 2
