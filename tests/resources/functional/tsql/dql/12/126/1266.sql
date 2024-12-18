-- tsql sql:
WITH customer_sales AS ( SELECT c_custkey, c_name, total_sales FROM ( VALUES (1, 'John', 100.0), (2, 'Jane', 200.0) ) AS data (c_custkey, c_name, total_sales) ) SELECT * FROM customer_sales
