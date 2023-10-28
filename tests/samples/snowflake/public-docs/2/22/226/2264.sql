SELECT
  symbol,
  exchange,
  cume_dist() OVER (PARTITION BY exchange ORDER BY price) AS cume_dist
FROM trades;
