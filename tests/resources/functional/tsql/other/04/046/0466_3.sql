--Query type: DCL
EXECUTE AS USER = 'User2';
WITH temp_result AS (
    SELECT '1-URGENT' AS priority, 100 AS price, '1993-01-01' AS order_date, 1 AS ship_priority
    UNION ALL
    SELECT '2-HIGH' AS priority, 200 AS price, '1993-01-02' AS order_date, 2 AS ship_priority
    UNION ALL
    SELECT '3-MEDIUM' AS priority, 300 AS price, '1993-01-03' AS order_date, 3 AS ship_priority
),
temp_result2 AS (
    SELECT '1-URGENT' AS priority, 100 AS price, '1993-01-01' AS order_date, 1 AS ship_priority
    UNION ALL
    SELECT '2-HIGH' AS priority, 200 AS price, '1993-01-02' AS order_date, 2 AS ship_priority
    UNION ALL
    SELECT '3-MEDIUM' AS priority, 300 AS price, '1993-01-03' AS order_date, 3 AS ship_priority
)
SELECT
    CASE
        WHEN SUM(CASE WHEN t1.priority = '1-URGENT' OR t1.priority = '2-HIGH' THEN 1 ELSE 0 END) > 0 THEN 'High'
        ELSE 'Low'
    END AS order_priority,
    SUM(t1.price * (1 - 0.1)) AS revenue,
    t1.order_date,
    t1.ship_priority
FROM temp_result t1
JOIN temp_result2 t2 ON t1.order_date = t2.order_date
WHERE t1.order_date >= '1993-01-01' AND t1.order_date < '1994-01-01'
GROUP BY t1.order_date, t1.ship_priority
HAVING SUM(t1.price * (1 - 0.1)) > 100000
ORDER BY revenue DESC, t1.order_date
OFFSET 0 ROWS
FETCH NEXT 10 ROWS ONLY;
