--Query type: DQL
WITH temp_result AS ( SELECT o_orderkey, o_totalprice FROM orders ) SELECT * FROM temp_result WHERE o_totalprice < ( SELECT AVG(o_totalprice) FROM orders );