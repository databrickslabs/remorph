SELECT
  listing_name,
  listing_display_name,
  event_date,
  SUM(IFF(event_type = 'LISTING CLICK', consumer_accounts_daily, 0)) AS listing_clicks,
  SUM(IFF(event_type IN ('GET', 'REQUEST') and action = 'STARTED', consumer_accounts_daily, 0)) AS get_request_started,
  SUM(IFF(event_type IN ('GET', 'REQUEST') and action = 'COMPLETED', consumer_accounts_daily, 0)) AS get_request_completed,
  get_request_completed / NULLIFZERO(listing_clicks) AS ctr
FROM snowflake.data_sharing_usage.LISTING_TELEMETRY_DAILY
GROUP BY 1,2,3
ORDER BY 1,2,3;