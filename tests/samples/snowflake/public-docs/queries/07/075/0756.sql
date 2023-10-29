-- see https://docs.snowflake.com/en/sql-reference/data-sharing-usage/listing-auto-fulfillment-refresh-daily

SELECT
   fulfillment_group_name,
   databases,
   listings,
   SUM(credits_used) AS total_credits_used
FROM snowflake.data_sharing_usage.listing_auto_fulfillment_refresh_daily
GROUP BY 1,2,3
ORDER BY 4 DESC;