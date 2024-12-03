--Query type: DQL
WITH customer_sales AS (
    SELECT c_custkey, c_name, SUM(EXTENDEDPRICE * (1 - DISCOUNT)) AS total_sales
    FROM (
        VALUES (1, 'Customer1', 100.0, 0.1),
               (2, 'Customer2', 200.0, 0.2),
               (3, 'Customer3', 300.0, 0.3)
    ) AS c (c_custkey, c_name, EXTENDEDPRICE, DISCOUNT)
    GROUP BY c_custkey, c_name
),
region_sales AS (
    SELECT r_regionkey, r_name, SUM(total_sales) AS region_total_sales
    FROM (
        VALUES (1, 'Region1', 1),
               (2, 'Region2', 2),
               (3, 'Region3', 3)
    ) AS r (r_regionkey, r_name, c_custkey)
    INNER JOIN customer_sales cs ON r.c_custkey = cs.c_custkey
    GROUP BY r_regionkey, r_name
)
SELECT rs.r_regionkey, rs.r_name, cs.c_name, cs.total_sales
FROM region_sales rs
INNER JOIN customer_sales cs ON rs.r_regionkey = cs.c_custkey
WHERE cs.total_sales > 1000 AND cs.c_name NOT LIKE N'%Customer%'
ORDER BY rs.region_total_sales DESC;
