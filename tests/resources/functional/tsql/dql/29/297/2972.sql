-- tsql sql:
WITH customer_regions AS (
    SELECT region_id, region_name
    FROM (
        VALUES (1, 'North'),
               (2, 'South'),
               (3, 'East'),
               (4, 'West')
    ) AS regions (region_id, region_name)
),
     customer_nations AS (
    SELECT nation_id, nation_name
    FROM (
        VALUES (1, 'USA'),
               (2, 'Canada'),
               (3, 'Mexico'),
               (4, 'UK')
    ) AS nations (nation_id, nation_name)
)
SELECT cr.region_name
FROM customer_regions AS cr
INNER JOIN customer_nations AS cn ON cr.region_id = cn.nation_id
WHERE cn.nation_name = 'USA';
