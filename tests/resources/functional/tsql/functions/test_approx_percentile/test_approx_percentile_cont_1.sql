-- Note that TSQL uses a continuous distribution model and requires an ORDER BY clause.
-- Databricks uses an approximate distribution algorithm, and does not require an ORDER BY clause.
-- The results may differ slightly due to the difference, but as teh result from both is an approximation,
-- the difference is unlikely to be significant.

-- tsql sql:
SELECT APPROX_PERCENTILE_CONT(col1, 0.5) WITHIN GROUP (ORDER BY something) AS approx_percentile_col1 FROM tabl;

-- databricks sql:
SELECT APPROX_PERCENTILE(col1, 0.5) AS approx_percentile_col1 FROM tabl;
