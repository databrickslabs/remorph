SELECT 
        store_ID, profit, 
        100 * RATIO_TO_REPORT(profit) OVER () AS percent_profit
    FROM store_profit
    ORDER BY store_ID;