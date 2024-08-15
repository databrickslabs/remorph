
-- snowflake sql:
SELECT symbol, exchange, shares, ROW_NUMBER() OVER (PARTITION BY exchange ORDER BY shares RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS row_number FROM trades;

-- databricks sql:
SELECT symbol, exchange, shares, ROW_NUMBER() OVER (PARTITION BY exchange ORDER BY shares NULLS LAST RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS row_number FROM trades;
