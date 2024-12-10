-- tsql sql:
WITH customer_info AS ( SELECT c_name, c_phone FROM ( VALUES ('Customer#000000001', '17-770-935-2891'), ('Customer#000000002', '13-570-314-2581') ) AS customer ( c_name, c_phone ) ) SELECT c_name FROM customer_info WHERE c_name LIKE '%#00000000%';
