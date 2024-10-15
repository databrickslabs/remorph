-- snowflake sql:
SELECT
  symbol,
  exchange,
  shares,
  ROW_NUMBER() OVER (
    PARTITION BY exchange
    ORDER BY
      shares
  ) AS row_number
FROM
  trades;

-- databricks sql:
SELECT
  symbol,
  exchange,
  shares,
  ROW_NUMBER() OVER (
    PARTITION BY exchange
    ORDER BY
      shares ASC NULLS LAST
  ) AS row_number
FROM
  trades;
