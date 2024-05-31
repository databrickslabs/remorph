
-- presto sql:
SELECT approx_percentile(height, weight, 0.5, 0.09) FROM people;

-- databricks sql:
SELECT approx_percentile(height, weight, 0.5, 1111 ) FROM people;

