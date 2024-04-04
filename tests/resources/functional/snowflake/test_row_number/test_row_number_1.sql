
-- snowflake sql:
SELECT symbol, exchange, shares, ROW_NUMBER() OVER (PARTITION BY exchange) AS row_number FROM trades;

-- databricks sql:
SELECT symbol, exchange, shares, ROW_NUMBER() OVER (PARTITION BY exchange) AS row_number FROM trades;
