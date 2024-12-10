-- tsql sql:
WITH cte AS (
    SELECT
        CASE
            WHEN l_discount > 0.05 THEN 'High'
            WHEN l_discount > 0.03 THEN 'Medium'
            ELSE 'Low'
        END AS discount_level,
        SUM(l_extendedprice) AS total_revenue,
        AVG(l_extendedprice * (1 - l_discount)) AS average_revenue,
        MAX(l_extendedprice) AS max_revenue,
        MIN(l_extendedprice) AS min_revenue,
        COUNT(l_orderkey) AS num_orders,
        GROUPING(l_shipmode) AS grouping
    FROM
        (
            VALUES
                (0.06, 100, 'AIR', 1),
                (0.04, 200, 'AIR', 2),
                (0.07, 300, 'TRUCK', 3),
                (0.05, 400, 'TRUCK', 4),
                (0.03, 500, 'MAIL', 5)
        ) AS t(l_discount, l_extendedprice, l_shipmode, l_orderkey)
    GROUP BY
        ROLLUP(l_discount, l_shipmode)
    HAVING
        SUM(l_extendedprice) > 500
)
SELECT
    discount_level,
    total_revenue,
    average_revenue,
    max_revenue,
    min_revenue,
    num_orders,
    grouping
FROM
    cte
ORDER BY
    discount_level,
    total_revenue DESC;
