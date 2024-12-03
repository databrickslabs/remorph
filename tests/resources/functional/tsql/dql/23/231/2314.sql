--Query type: DQL
WITH CustomerData AS ( SELECT c_custkey, c_name, c_address FROM ( VALUES (1, 'Customer#001', '123 Main St'), (2, 'Customer#002', '456 Elm St') ) AS Customer(c_custkey, c_name, c_address) ) SELECT * FROM CustomerData;
