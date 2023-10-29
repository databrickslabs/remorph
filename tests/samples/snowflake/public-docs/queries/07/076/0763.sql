-- see https://docs.snowflake.com/en/sql-reference/functions/percent_rank

SELECT
  exchange,
  symbol,
  PERCENT_RANK() OVER (PARTITION BY exchange ORDER BY price) AS percent_rank
FROM trades;
