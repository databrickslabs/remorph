-- tsql sql:
SELECT TOP (31) WITH TIES c_name, c_address FROM ( VALUES ('Customer1', 'Address1'), ('Customer2', 'Address2'), ('Customer3', 'Address3') ) AS Customer (c_name, c_address) ORDER BY c_address;