--Query type: DQL
SELECT (CASE WHEN c_custkey > 10 THEN c_name ELSE c_address END) AS customer_info FROM (VALUES (1, 'Customer1', 'Address1'), (2, 'Customer2', 'Address2'), (3, 'Customer3', 'Address3'), (11, 'Customer11', 'Address11'), (12, 'Customer12', 'Address12')) AS customers (c_custkey, c_name, c_address);
