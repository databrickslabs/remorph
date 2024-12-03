--Query type: DQL
WITH customer_regions AS ( SELECT 'North' AS region, 1 AS customer_id UNION ALL SELECT 'South' AS region, 2 AS customer_id ) SELECT o.name, cr.region, o.order_total FROM customer_regions cr INNER JOIN ( VALUES ( 1, 'Customer1', 100.0 ), ( 2, 'Customer2', 200.0 ) ) AS o ( customer_id, name, order_total ) ON cr.customer_id = o.customer_id WHERE cr.region = 'North';
