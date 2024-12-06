-- tsql sql:
WITH temp_result AS ( SELECT * FROM ( VALUES (1, 100), (2, 200), (3, 300) ) AS t (c_custkey, o_orderkey) ) SELECT * FROM temp_result.ufn_GetOrderDetails (100);
