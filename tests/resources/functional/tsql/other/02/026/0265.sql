--Query type: DDL
WITH customer_view AS ( SELECT c_custkey AS [Customer Key], c_name AS [Customer Name], c_address AS [Customer Address] FROM (VALUES (1, 'Customer1', 'Address1'), (2, 'Customer2', 'Address2')) AS customer(c_custkey, c_name, c_address) ) SELECT * FROM customer_view;
