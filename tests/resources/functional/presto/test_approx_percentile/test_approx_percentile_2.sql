
-- presto sql:
SELECT approx_percentile(height, 0.5, 0.01) FROM people;

-- databricks sql:
SELECT approx_percentile(height, 0.5, 10000) FROM people;
