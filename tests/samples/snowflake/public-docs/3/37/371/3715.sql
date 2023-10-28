SELECT
  *,
  ROW_NUMBER() OVER (PARTITION BY listing_name, listing_display_name ORDER BY jobs DESC) AS rank
FROM (
  SELECT
    listing_name,
    listing_display_name,
    consumer_account_locator,
    SUM(jobs) AS jobs
  FROM snowflake.data_sharing_usage.listing_consumption_daily
  WHERE 1=1
    AND event_date BETWEEN '2021-01-01' AND '2021-01-31'
  GROUP BY 1,2,3
)
ORDER BY
  listing_name,
  listing_display_name,
  rank