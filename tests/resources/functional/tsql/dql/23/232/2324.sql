--Query type: DQL
WITH cte AS (SELECT * FROM (VALUES (1, 'customer1'), (2, 'customer2')) AS customer (customer_id, customer_name))
SELECT cte.customer_id, cte.customer_name
FROM cte
WHERE cte.customer_id = (SELECT customer_id FROM (VALUES (1, 'customer1'), (2, 'customer2')) AS customer (customer_id, customer_name) WHERE customer_name = 'customer1');
