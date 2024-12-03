--Query type: DQL
WITH temp_result AS ( SELECT * FROM ( VALUES (1, 'John'), (2, 'Jane') ) AS temp_table (id, name) ) SELECT * FROM temp_result ORDER BY id;
