--Query type: DQL
DECLARE customer_cursor CURSOR FOR SELECT c_custkey, c_name, c_address FROM (VALUES (1, 'Customer1', 'Address1'), (2, 'Customer2', 'Address2')) AS customers (c_custkey, c_name, c_address);
