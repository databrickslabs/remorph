SELECT branch_ID,
       net_profit,
       100 * RATIO_TO_REPORT(net_profit) OVER () AS percent_of_chain_profit
    FROM store_sales AS s1
    ORDER BY branch_ID;