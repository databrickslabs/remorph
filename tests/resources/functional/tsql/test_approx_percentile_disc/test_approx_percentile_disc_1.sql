-- APPROX_PERCENTILE_DISC
--
-- This function has no direct equivalent in Databricks. The closest equivalent is the PERCENTILE function.
-- Approximations are generally faster then exact calculations, so performance may be something to explore.

-- tsql sql:
SELECT APPROX_PERCENTILE_DISC(col1) AS approx_count_distinct_col1 FROM tabl;

-- databricks sql:
SELECT PERCENTILE(col1, 0.5) AS approx_count_distinct_col1 FROM tabl;
