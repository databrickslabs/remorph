--Query type: DDL
SELECT * FROM (VALUES (1, 'John', '123 Main St'), (2, 'Jane', '456 Elm St')) AS customer_cte (c_custkey, c_name, c_address);
