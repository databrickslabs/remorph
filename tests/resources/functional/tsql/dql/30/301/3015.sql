-- tsql sql:
WITH temp_result AS (
    SELECT r_name, SUM(o_totalprice) AS total_revenue
    FROM region
    INNER JOIN orders ON r_regionkey = o_orderpriority
    INNER JOIN customer ON o_custkey = c_custkey
    INNER JOIN lineitem ON l_orderkey = o_orderkey
    WHERE c_nationkey = r_regionkey
    GROUP BY r_name
)
SELECT r_name, PERCENTILE_DISC(0.10) WITHIN GROUP(ORDER BY total_revenue) OVER () AS 'P10', PERCENTILE_DISC(0.90) WITHIN GROUP(ORDER BY total_revenue) OVER () AS 'P90'
FROM temp_result
GROUP BY r_name
