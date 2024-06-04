
-- presto sql:
SELECT approx_percentile(height, weight, ARRAY[0.25, 0.5, 0.75], 0.9) FROM people;

-- databricks sql:
SELECT approx_percentile(height, weight, ARRAY(0.25, 0.5, 0.75), 111 ) FROM people;

