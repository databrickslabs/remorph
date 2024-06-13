
-- presto sql:
SELECT approx_percentile(height, ARRAY[0.25, 0.5, 0.75], 0.5) FROM people;

-- databricks sql:
SELECT approx_percentile(height, ARRAY(0.25, 0.5, 0.75), 200) FROM people;
