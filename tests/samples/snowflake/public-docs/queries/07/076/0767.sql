-- see https://docs.snowflake.com/en/sql-reference/functions/row_number

SELECT
  symbol,
  exchange,
  shares,
  ROW_NUMBER() OVER (PARTITION BY exchange ORDER BY shares) AS row_number
FROM trades;
