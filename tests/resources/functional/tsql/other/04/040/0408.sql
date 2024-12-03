--Query type: DDL
WITH temp_result AS (
    SELECT c_custkey, o_totalprice
    FROM (
        VALUES (1, 100000.0),
               (2, 50000.0),
               (3, 200000.0)
    ) AS customer(c_custkey, c_acctbal)
    JOIN (
        VALUES (1, 100000.0),
               (2, 50000.0),
               (3, 200000.0)
    ) AS orders(o_orderkey, o_totalprice)
    ON c_custkey = o_orderkey
)
SELECT
    CASE
        WHEN o_totalprice > 100000 THEN 'High'
        WHEN o_totalprice > 50000 THEN 'Medium'
        ELSE 'Low'
    END AS price_category,
    SUM(o_totalprice) AS total_revenue
FROM temp_result
GROUP BY
    CASE
        WHEN o_totalprice > 100000 THEN 'High'
        WHEN o_totalprice > 50000 THEN 'Medium'
        ELSE 'Low'
    END
ORDER BY total_revenue DESC;
