-- snowflake sql:
SELECT
  symbol,
  exchange,
  shares,
  ROW_NUMBER() OVER (
    PARTITION BY exchange
    ORDER BY
      shares DESC RANGE BETWEEN UNBOUNDED PRECEDING
      AND CURRENT ROW
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
      shares DESC NULLS FIRST RANGE BETWEEN UNBOUNDED PRECEDING
      AND CURRENT ROW
  ) AS row_number
FROM
  trades;
