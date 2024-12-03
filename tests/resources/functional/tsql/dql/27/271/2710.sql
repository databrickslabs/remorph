--Query type: DQL
WITH temp_result AS ( SELECT p_partkey, ps_supplycost, SUM(ol_extendedprice) AS total FROM ( VALUES (1, 10.0, 100.0), (2, 20.0, 200.0), (3, 30.0, 300.0) ) AS t (p_partkey, ps_supplycost, ol_extendedprice) GROUP BY p_partkey, ps_supplycost ) SELECT p_partkey, ps_supplycost, total FROM temp_result WHERE ps_supplycost < 5.00 ORDER BY p_partkey, ps_supplycost;
