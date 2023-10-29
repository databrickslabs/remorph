-- see https://docs.snowflake.com/en/sql-reference/functions/cume_dist

SELECT
  symbol,
  exchange,
  cume_dist() OVER (PARTITION BY exchange ORDER BY price) AS cume_dist
FROM trades;
