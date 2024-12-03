--Query type: DDL
WITH temp_table AS ( SELECT col1, CAST(NULL AS VARCHAR(50)) AS col2 FROM (VALUES (1)) AS temp_table(col1) ) SELECT * FROM temp_table;
