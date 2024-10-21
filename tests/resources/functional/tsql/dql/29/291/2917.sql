--Query type: DQL
SELECT c_name, c_address FROM (VALUES ('Customer#000000001', '1313 13th St'), ('Customer#000000002', '123 Main St')) AS customers (c_name, c_address)