SELECT
   databases,
   listings,
   SUM(credits_used) AS total_credits_used
FROM snowflake.data_sharing_usage.listing_auto_fulfillment_refresh_daily
WHERE 1=1
   AND usage_date BETWEEN '2023-04-17' AND '2023-04-30'
GROUP BY 1,2
ORDER BY 3 DESC;