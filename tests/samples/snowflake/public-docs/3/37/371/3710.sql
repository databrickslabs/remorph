SELECT
  listing_name,
  listing_display_name,
  event_date,
  event_type,
  SUM(1) AS count_gets_requests
FROM snowflake.data_sharing_usage.listing_events_daily
GROUP BY 1,2,3,4