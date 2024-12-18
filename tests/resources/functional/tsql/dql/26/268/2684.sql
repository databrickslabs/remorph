-- tsql sql:
WITH CustomerData AS ( SELECT c_custkey, c_name, c_address FROM (VALUES (1, 'Customer 1', 'Address 1'), (2, 'Customer 2', 'Address 2'), (3, 'Customer 3', 'Address 3') ) AS Customer(c_custkey, c_name, c_address) ) SELECT c_name, c_address, COALESCE(c_name, c_address) AS FirstNotNull FROM CustomerData;
