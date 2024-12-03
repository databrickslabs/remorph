--Query type: DQL
WITH temp_result AS ( SELECT * FROM ( VALUES (1, 'John'), (2, 'Jane') ) AS c (c_custkey, c_name) ) SELECT * FROM temp_result ORDER BY c_custkey;
