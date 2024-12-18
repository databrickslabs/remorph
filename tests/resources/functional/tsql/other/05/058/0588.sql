-- tsql sql:
WITH temp_result AS ( SELECT * FROM ( VALUES (1, 'a'), (2, 'b'), (3, 'c') ) AS t (id, name) ) SELECT * FROM temp_result;
