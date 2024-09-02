--Query type: DCL
WITH temp_result AS ( SELECT id FROM ( VALUES (1) ) AS temp_table (id) ) SELECT * FROM temp_result; DROP SCHEMA IF EXISTS customer_schema;