SELECT
   listing_name,
   listing_display_name,
   SUM(jobs) AS jobs
FROM snowflake.data_sharing_usage.listing_consumption_daily
WHERE 1=1
   AND event_date BETWEEN '2021-01-01' AND '2021-01-31'
GROUP BY 1,2
ORDER BY 3 DESC