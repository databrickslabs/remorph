SELECT
  exchange,
  symbol,
  PERCENT_RANK() OVER (PARTITION BY exchange ORDER BY price) AS percent_rank
FROM trades;
