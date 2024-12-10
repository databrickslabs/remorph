-- tsql sql:
WITH temp_result AS (
    SELECT 'province1' AS province, 1 AS store_ID, 100.0 AS profit
    UNION ALL
    SELECT 'province1' AS province, 2 AS store_ID, 200.0 AS profit
    UNION ALL
    SELECT 'province2' AS province, 3 AS store_ID, 300.0 AS profit
)
SELECT province, store_ID, profit, (profit * 100.0) / (SELECT SUM(profit) FROM temp_result tr2 WHERE tr2.province = tr1.province) AS percent_profit
FROM temp_result tr1
ORDER BY province, store_ID;
