SELECT
  symbol,
  exchange,
  shares,
  ROW_NUMBER() OVER (PARTITION BY exchange ORDER BY shares) AS row_number
FROM trades;
