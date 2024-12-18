-- tsql sql:
WITH customer_data AS ( SELECT * FROM ( VALUES ('Customer#1', 100), ('Customer#2', 200) ) AS data ( customer_name, customer_id ) ) SELECT customer_name, customer_id FROM customer_data
