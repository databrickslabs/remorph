-- tsql sql:
WITH CustomerCTE AS ( SELECT c_custkey, c_name, c_address FROM ( VALUES (1, 'Customer1', 'Address1'), (2, 'Customer2', 'Address2') ) AS Customer (c_custkey, c_name, c_address) ) SELECT c_name, c_address FROM CustomerCTE WHERE c_name = 'Customer1';
