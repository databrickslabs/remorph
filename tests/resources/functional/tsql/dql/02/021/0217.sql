--Query type: DQL
WITH customer AS ( SELECT * FROM ( VALUES (1, 'John', 'Doe'), (2, 'Jane', 'Doe') ) AS customer (customer_id, first_name, last_name) ) SELECT * FROM customer;
