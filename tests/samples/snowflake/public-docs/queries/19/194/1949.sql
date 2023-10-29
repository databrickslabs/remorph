-- see https://docs.snowflake.com/en/sql-reference/functions/approx_top_k

WITH states AS (
  SELECT approx_top_k(C4, 3, 5) AS state
  FROM lineitem
)
SELECT value[0]::INT AS value, value[1]::INT AS frequency
FROM states, LATERAL FLATTEN(state);
