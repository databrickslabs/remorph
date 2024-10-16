--Query type: DQL
WITH customer_names AS ( SELECT 'Customer#000000001' AS name UNION ALL SELECT 'Customer#000000002' AS name ) SELECT name, REVERSE(name) AS reversed_name FROM customer_names;