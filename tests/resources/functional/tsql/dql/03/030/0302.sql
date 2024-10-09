--Query type: DQL
WITH temp_result AS (
    SELECT 1000 AS order_total, 10 AS quantity
    UNION ALL
    SELECT 2000 AS order_total, 20 AS quantity
    UNION ALL
    SELECT 3000 AS order_total, 30 AS quantity
)
SELECT STDEVP(DISTINCT order_total) AS Distinct_Values, STDEVP(order_total) AS All_Values
FROM temp_result;