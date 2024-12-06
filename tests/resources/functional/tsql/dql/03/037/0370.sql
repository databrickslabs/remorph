-- tsql sql:
WITH customer_info AS ( SELECT c_custkey, c_name, c_phone FROM ( VALUES (1, 'Customer1', '123-456-7890'), (2, 'Customer2', '987-654-3210') ) AS customer (c_custkey, c_name, c_phone) ) SELECT c_custkey, c_name, c_phone FROM customer_info WHERE c_phone LIKE '%123%' OR c_phone LIKE '%987%';
