--Query type: DDL
WITH customer_cte AS ( SELECT c_custkey, c_name, c_address FROM customer ) SELECT * FROM customer_cte;