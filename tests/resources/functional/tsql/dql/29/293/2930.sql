--Query type: DQL
WITH customer_regions AS (
    SELECT region_id, region_name
    FROM (
        VALUES (1, 'North'),
               (2, 'South'),
               (3, 'East'),
               (4, 'West')
    ) AS regions (region_id, region_name)
),
orders AS (
    SELECT order_id, customer_id, order_date
    FROM (
        VALUES (1, 1, '2020-01-01'),
               (2, 2, '2020-01-15'),
               (3, 3, '2020-02-01')
    ) AS orders (order_id, customer_id, order_date)
)
SELECT cr.region_id AS [region_num],
       o.order_id,
       o.order_date
FROM customer_regions AS cr
INNER JOIN orders AS o
    ON cr.region_id = o.customer_id
    AND o.order_date > '2020-01-01';