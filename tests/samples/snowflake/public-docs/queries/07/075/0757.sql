-- see https://docs.snowflake.com/en/sql-reference/data-sharing-usage/listing-auto-fulfillment-database-storage-daily

SELECT
   snowflake_region,
   database_name,
   listings,
   SUM(average_database_bytes) AS total_storage
FROM snowflake.data_sharing_usage.listing_auto_fulfillment_database_storage_daily
WHERE 1=1
   AND usage_date BETWEEN '2023-04-17' AND '2023-04-30'
GROUP BY 1,2,3
ORDER BY 4 DESC;