-- ##APPROX_COUNT_DISTINCT
--
-- This function is identical to the APPROX_COUNT_DISTINCT function in Databricks. Though
-- the syntax is the same, the results may differ slightly due to the difference in the implementations
-- and the fact that it is an approximation.

-- tsql sql:
SELECT APPROX_COUNT_DISTINCT(col1) AS approx_count_distinct_col1 FROM tabl;

-- databricks sql:
SELECT APPROX_COUNT_DISTINCT(col1) AS approx_count_distinct_col1 FROM tabl;
