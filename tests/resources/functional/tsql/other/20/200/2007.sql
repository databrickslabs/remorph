-- tsql sql:
DROP PROCEDURE pr_Names;

WITH temp_result AS (
    SELECT '1-URGENT' AS order_priority, 100 AS revenue, '1993-01-01' AS order_date, 1 AS ship_priority
    UNION ALL
    SELECT '2-HIGH' AS order_priority, 200 AS revenue, '1993-01-02' AS order_date, 2 AS ship_priority
    UNION ALL
    SELECT '3-MEDIUM' AS order_priority, 300 AS revenue, '1993-01-03' AS order_date, 3 AS ship_priority
)

SELECT
    CASE
        WHEN order_priority = '1-URGENT' OR order_priority = '2-HIGH' THEN 'High'
        ELSE 'Low'
    END AS order_priority,
    SUM(revenue) AS total_revenue,
    order_date,
    ship_priority
FROM temp_result
WHERE order_date >= '1993-01-01' AND order_date < '1994-01-01'
GROUP BY
    CASE
        WHEN order_priority = '1-URGENT' OR order_priority = '2-HIGH' THEN 'High'
        ELSE 'Low'
    END,
    order_date,
    ship_priority
ORDER BY total_revenue DESC, order_date
OFFSET 0 ROWS
FETCH NEXT 10 ROWS ONLY;
