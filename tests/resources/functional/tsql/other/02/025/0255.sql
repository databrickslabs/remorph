-- tsql sql:
WITH temp_table AS ( SELECT id FROM ( VALUES (1) ) AS id(id) ) SELECT * FROM temp_table;
