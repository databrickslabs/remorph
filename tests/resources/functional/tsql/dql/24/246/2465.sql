-- tsql sql:
SELECT CONCAT_WS(' - ', c_custkey, c_name, c_address) AS CustomerInfo FROM (VALUES (1, 'Customer1', 'Address1'), (2, 'Customer2', 'Address2')) AS Customer(c_custkey, c_name, c_address);
