-- tsql sql:
WITH customer AS ( SELECT c_custkey, c_name FROM ( VALUES (1, 'Customer1'), (2, 'Customer2') ) AS customer(c_custkey, c_name) ) SELECT c_custkey, c_name FROM customer WHERE c_custkey > 1;