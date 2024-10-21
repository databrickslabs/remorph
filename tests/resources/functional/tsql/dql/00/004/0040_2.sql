--Query type: DQL
WITH temp_result AS ( SELECT * FROM ( VALUES (1, 'customer1'), (2, 'customer2') ) AS customers (customer_id, customer_name) ) SELECT * FROM temp_result;