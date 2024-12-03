--Query type: DDL
WITH Customer AS ( SELECT c_custkey, c_name, c_address FROM ( VALUES (1, 'John', '123 Main St'), (2, 'Jane', '456 Elm St') ) AS Customer (c_custkey, c_name, c_address) ) SELECT * FROM Customer;
