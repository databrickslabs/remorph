
-- presto sql:
SELECT approx_percentile(height, weight, 0.5, 'non_integer') FROM people;

-- databricks sql:
SELECT approx_percentile(height, weight, 0.5, 0.01) FROM people;
