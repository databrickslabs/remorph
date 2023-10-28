SELECT 
        province, store_ID, profit, 
        100 * RATIO_TO_REPORT(profit) OVER (PARTITION BY province) AS percent_profit
    FROM store_profit
    ORDER BY province, store_ID;