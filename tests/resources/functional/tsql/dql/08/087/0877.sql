--Query type: DQL
WITH temp_result AS ( SELECT * FROM ( VALUES ('O1', 'P1'), ('O2', 'P2') ) AS t (o_orderkey, o_orderpriority) ) SELECT * FROM temp_result;