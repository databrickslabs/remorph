--Query type: DQL
SELECT c_customer_sk, c_first_name FROM (VALUES (1, 'John'), (2, 'Mary'), (3, 'David')) AS customers (c_customer_sk, c_first_name) WHERE c_first_name LIKE 'J%';
